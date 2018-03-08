import json
import requests
from thingiverse.utils import parse_link, Config

class ThingiverseBase():
	def __init__(self, config=None):
		if config:
			self.config = config
		else:
			self.config = Config.fetch_config("access_token")

	def get(self, url):
		headers = {'Authorization': "%s %s" % (
			self.config['token_type'],
			self.config['access_token'])}
		return requests.get(url, headers=headers)

	def post(self, url, **kwargs):
		headers = {'Authorization': "%s %s" % (
			self.config['token_type'],
			self.config['access_token'])}
		return requests.post(url, headers=headers, data=json.dumps(kwargs))

	def patch(self, url, **kwargs):
		headers = {'Authorization': "%s %s" % (
			self.config['token_type'],
			self.config['access_token'])}
		return requests.patch(url, headers=headers, data=json.dumps(kwargs))

class Thingiverse(ThingiverseBase):
	def get_my_things(self):
		url = "https://api.thingiverse.com/users/me/things"
		r = self.get(url)
		things = json.loads(r.text)
		for thing in things:
			yield thing
		links = parse_link(r.headers['Link'])
		while links.has_key('next'):
			r = self.get(links['next'])
			things = json.loads(r.text)
			for thing in things:
				yield thing
			links = parse_link(r.headers['Link'])

	def get_thing(self, thing):
		if thing.has_key('url'):
			r = self.get(thing['url'])
			thing = json.loads(r.text)
			return Thing(thing)
		elif thing.has_key('id'):
			url = "https://api.thingiverse.com/things/%s" % thing['id']
			r = self.get(url)
			thing = json.loads(r.text)
			return Thing(thing)

	def create_thing(self, **kwargs):
		url = "https://api.thingiverse.com/things/"
		r = self.post(url, **kwargs)
		thing = json.loads(r.text)
		return Thing(thing)

class Thing(ThingiverseBase):
	def __init__(self, thing, config=None):
		self.thing = thing
		ThingiverseBase.__init__(self)

	def __getattr__(self, name):
		if name.startswith("get_"):
			def get_subobject():
				field = name[4:]
				r = self.get(self.thing["%s_url" %(field)])
				self.thing[field] = json.loads(r.text)
			return get_subobject
		return self.thing[name]

	def __getitem__(self, name):
		return self.thing[name]

	def to_json(self, **kwargs):
		return json.dumps(self.thing, **kwargs)

	def update(self, **kwargs):
		url = "https://api.thingiverse.com/things/%s" % self.thing['id']
		r = self.patch(url, **kwargs)
		thing = json.loads(r.text)
		return Thing(thing)
