
from datetime import datetime

import sqlalchemy as sa

from gino.ext.sanic import Gino
from sqlalchemy.engine.url import URL

db = Gino()


class Book(db.Model):
	__tablename__ = "books"
	__table_args__ = (
		sa.UniqueConstraint("name", "author", "existent"),
	)

	id = sa.Column(sa.Integer, primary_key=True)
	name = sa.Column(sa.String(255), index=True, nullable=False)
	author = sa.Column(sa.String(255), index=True, nullable=False)
	rating = sa.Column(sa.Integer, nullable=False)
	time = sa.Column(sa.DateTime, default=datetime.utcnow)
	existent = sa.Column(sa.Boolean, default=True)

	@classmethod
	def fetch_unhiden(cls, pk):
		return cls.query.where(
			Book.id == int(pk)
		).where(
			Book.existent == True
		).gino.first()

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"author": self.author,
			"rating": self.rating,
			"time": self.time
		}


async def init(conf):
	conf = conf["db"]
	conn_str = "postgresql://{user}:{password}@{host}/{name}".format(**conf)

	async with db.with_bind(conn_str):
		await db.gino.create_all()
