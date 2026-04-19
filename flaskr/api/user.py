from flask import Blueprint, request
import json
import uuid
from .. import jwtman

user_bp = Blueprint('user', __name__, url_prefix='/api')

def respond_error (message):
    return json.dumps({
        'success': False,
        'error': message,
	})

def respond_success ():
    return json.dumps({
        'success': True,
        'error': None,
	})

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
        return respond_error('Invalid JWT')
    
    book_name = data.get('name')
    book_author = data.get('author')
    book_desc = data.get('desc')
    isbn = data.get('isbn')
    zip_code = data.get('zip_code')

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
                'user': user['id'],
            }

            new_book = {
                'id': book_id,
                'zip_code': zip_code,
                'name': book_name,
                'author': book_author,
                'desc': book_desc,
                'isbn': isbn,
                'owner': user['id'],
                'status_record': record_id
            }

            books_db.append(new_book)
            books_fp.seek(0)
            books_fp.write(json.dumps(books_db))
            books_fp.truncate()
            
            records_db.append(new_record)
            records_fp.seek(0)
            records_fp.write(json.dumps(records_db))
            records_db.truncate()
            return respond_success(), 200
            
    
    return respond_error("Unknown error"), 400
