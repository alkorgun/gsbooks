# Book library project

Book library Web API written in Python, [Sanic](https://github.com/huge-success/sanic) & [Gino](https://github.com/fantix/gino).

## Run

```bash
sudo docker-compose up
```

## API

* GET /book — show all books.

```sh
curl -v -w "\n" localhost:8080/book
```

* GET /book/`<id>` — show a book.

```sh
curl -v -w "\n" localhost:8080/book/1
```

* POST /book — create a book.

```sh
curl -v -w "\n" -X POST -d '{"name": "Garrett P.I.", "author": "Glen Cook", "rating": 9}' localhost:8080/book
```

* PATCH /book/`<id>` — update a book.

```sh
curl -v -w "\n" -X PATCH -d '{"rating": 10}' localhost:8080/book/1
```

* DELETE /book/`<id>` — delete a book.

```sh
curl -v -w "\n" -X DELETE localhost:8080/book/1
```

### JSON fields

* `id` — an unique identifier.
* `name` — a book name.
* `author` — an author.
* `rating` — a book rating.
* `time` — an update time.

### POST / PATCH limitations

* `name: varchar(255)`
* `author: varchar(255)`
* `rating: 0 < integer < 11`
