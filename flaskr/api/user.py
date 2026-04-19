from flask import Blueprint, request
import json
import uuid
from .. import jwtman

user_bp = Blueprint('user', __name__, url_prefix='/api')

def check_jwt_data(encoded_jwt):
    id = jwtman.jwt_tok_validate(encoded_jwt)
    with open("flaskr/data/users.json", "r") as users_fp:
        users_db = json.load(users_fp)
        user_found = next((user for user in users_db if ((user['id'] == id))), False)
        return user_found

@user_bp.route('self/add_book', methods=['POST'])
def request_checkout():
    data = request.json
    encoded_jwt = data.get('jwt')
    user = check_jwt_data(encoded_jwt)
    if not user:
        return error_return("Invalid jwt")
    
    book_name = data.get('name')
    book_author = data.get('author')
    book_desc = data.get('desc')
    isbn = data.get('isbn')
    zip_code = data.get('iszip_codebn')

    with open("flaskr/data/books.json", "r+") as books_fp:
        books_db = json.load(books_fp)
        with open("flaskr/data/records.json", "r+") as records_fp:
            records_db = json.load(records_fp)
            record_id = str(uuid.uuid4())
            book_id = str(uuid.uuid4())

            new_record = {
                'id': record_id,
                'type': 'added',
                'book': book_id,
                'user': 'None'
            }

            new_book = {
                'id': book_id,
                'zip_code': zip_code,
                'name': book_name,
                'author': book_author,
                'desc': book_desc,
                'isbn': isbn,
                'owner': user['username'],
                'status_record': record_id
            }

            books_db.append(new_book)
            records_db.append(new_record)
            books_fp.seek(0)
            books_fp.write(json.dumps(books_db))
            records_fp.seek(0)
            records_fp.write(json.dumps(records_db))
            return 'success', 200
            
    
    return 'test', 400
