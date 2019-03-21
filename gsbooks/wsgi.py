
from datetime import datetime

from sanic import Sanic
from sanic.response import json
from sqlalchemy.exc import DatabaseError, IntegrityError
from asyncpg.exceptions import DataError, UniqueViolationError

from .db import db, Book

app = Sanic(__name__)

_w_cols = ("name", "author", "rating")


def error(status, *args, **kwargs):
	"""
	A shortcut for empty json result.
	"""
	return json({}, status)


@app.post("/book")
async def create_book(request):
	if not isinstance(request.json, dict):
		return error(400, "bad request (list)")
	try:
		kwargs = {k: request.json[k] for k in _w_cols}
	except KeyError:
		return error(400, "bad request")

	if not (0 < kwargs["rating"] < 11):
		return error(400, "bad request")

	book = Book(**kwargs)

	try:
		await book.create()
	except DataError:
		return error(400, "bad request")
	except UniqueViolationError:
		return error(400, "book already exists")
	except DatabaseError:
		return error(500, "db error")
	return json(book.to_dict())


@app.get("/book")
async def get_books_list(request):
	try:
		books = await Book.query.where(Book.existent == True).gino.all()
	except DatabaseError:
		return error(500, "db error")
	return json([b.to_dict() for b in books])


@app.get("/book/<pk:int>")
async def get_book(request, pk):
	book = await Book.fetch_existent(int(pk))
	if not book:
		return error(404, "no such book")
	return json(book.to_dict())


@app.patch("/book/<pk:int>")
async def patch_book(request, pk):
	if not isinstance(request.json, dict):
		return error(400, "bad request (list)")

	book = await Book.fetch_existent(int(pk))
	if not book:
		return error(404, "no such book")

	kwargs = {k: request.json.get(k, getattr(book, k)) for k in _w_cols}

	if not (0 < kwargs["rating"] < 11):
		return error(400, "bad request")

	try:
		await book.update(time=datetime.utcnow(), **kwargs).apply()
	except DataError:
		return error(400, "bad request")
	except UniqueViolationError:
		return error(400, "book like this already exists")
	except DatabaseError:
		return error(500, "db error")
	return json(book.to_dict())


@app.delete("/book/<pk:int>")
async def delete_book(request, pk):
	book = await Book.fetch_existent(int(pk))
	if not book:
		return error(404, "no such book")
	try:
		await book.update(
			time=datetime.utcnow(),
			existent=None
		).apply()
	except DatabaseError:
		return error(500, "db error")
	return json({})
