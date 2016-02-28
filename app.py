from flask import Flask, request, render_template, flash, redirect, url_for, Markup
from flask.ext.pymongo import PyMongo
from flask_wtf.csrf import CsrfProtect
from forms import URLForm
import string
import random

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'links'

#some basic security, used random passwords instead of a more secure one for this example
app.config['SECRET_KEY'] = '!xsmkOZDGs\1EKgsO5eR1<OHO*lNFz'
app.config['SECURITY_PASSWORD_SALT'] = ')2 .D~756R:G^0v2yOx\$>SDpN/\dN'

mongo = PyMongo(app)
CsrfProtect(app)

@app.route('/', methods=('GET',))
def homepage():
	form = URLForm()
	return render_template('index.html', form=form)

@app.route('/create-url', methods=('POST',))
def create():
	form = URLForm()
	if request.method =='POST':
		if form.validate():
			try:
				#check if site in database, if not create a new document
				site_id = mongo.db.links.find_one_or_404({'url':form.url.data})['site_id']
			except:
				#not the best way to do this, but for demonstrations purposes it gets the job done.
				site_id = ''
				for i in range(random.randrange(3,6)):
					site_id += random.choice(string.ascii_letters)

				data = {
					'site_id': site_id,
					'url': form.url.data
				}
				mongo.db.links.insert(data)
			
			flash('URL created! <a href="{0}" target="_blank">{0}</a> redirects to {1}.'.format(url_for("homepage", _external=True) + site_id, form.url.data))
			return redirect(url_for('homepage'))

@app.route('/<site_id>')
def shortner(site_id):
	try:
		link = mongo.db.links.find_one_or_404({'site_id':site_id})
		return redirect(link['url'])
	except:
		return redirect(url_for('homepage'))