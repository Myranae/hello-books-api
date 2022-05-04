from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book

books_bp = Blueprint("books", __name__, url_prefix="/books")

# HELPER FUNCTIONS
# validate book data is correct
def validate_book(book_id):
    # handle non-int input for book_id
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"message":f"book id '{book_id}' is invalid"}, 400))

    # handle no entry for book_id requested
    book = Book.query.get(book_id)
    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))
    return book

# ROUTES
# create one book
@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return "Invalid Request ", 400
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"]
        )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book '{new_book.title}' successfully created"), 201)

# get all books
@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")

    if title_query is not None:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description,
            }
        )
    return make_response(jsonify(books_response), 200)

# get a single book
@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {
                "id": book.id,
                "title": book.title,
                "description": book.description,
            }

# replace all the info of one record
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book {book_id} successfully updated"), 200)

# delete one record
@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)

    db.session.commit()

    return make_response(jsonify("Book {book_id} successfully deleted"), 200)