from flask import session
from flask.ext.wtf import Form
from wtforms import validators, StringField
import requests

class URLForm(Form):
	url = StringField('website_url', [validators.Required()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if self.url.data:
			try:
				if requests.head(self.url.data).status_code in (200, 301):
					return True
			except:
				return False
		return False