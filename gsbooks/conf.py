
import json

from .wsgi import app, db

CONF_FILE = "/etc/gsbooks/gsbooks.json"


def get(filename=CONF_FILE):
	"""
	Get configuration from a json file.
	"""
	with open(filename) as fp:
		return json.load(fp)


def configure(filename=None):
	"""
	Apply configuration from a json file.
	"""
	if filename:
		conf = get(filename=filename)
	else:
		conf = get()
	apply(conf)


def apply(conf):
	"""
	Apply configuration from a dict.
	"""
	_db = conf["db"]
	app.config.DB_HOST     = _db["host"]
	app.config.DB_PORT     = _db["port"]
	app.config.DB_DATABASE = _db["name"]
	app.config.DB_USER     = _db["user"]
	app.config.DB_PASSWORD = _db["password"]

	db.init_app(app)
