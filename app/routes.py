
from xml.dom import ValidationErr
from flask import Blueprint, jsonify, abort, make_response

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Red Fish, Blue Fish", "A Dr. Seuss book"),
    Book(2, "The Grinch", "Another Dr. Seuss book"),
    Book(3, "The Lorax", "The best Dr. Seuss book"),
]

# hello_world_bp = Blueprint("hello_world_bp", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({"message":f"book id {book_id} is invalid"}, 400))
    for book in books:
        if book.id == book_id:
            return book
    abort(make_response({"message":"book {book_id} not found"}, 404))

@books_bp.route("", methods=["GET"])
def all_books():
    books_json = []
    for book in books:
        books_json.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description,
            }
        )
    return jsonify(books_json), 200 

@books_bp.route("/<book_id>", methods=["GET"])
def get_book(book_id):
    book = validate_book(book_id)
    return {
                "id": book.id,
                "title": book.title,
                "description": book.description,
            }

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     return "Hello, World!"


# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }


# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body
