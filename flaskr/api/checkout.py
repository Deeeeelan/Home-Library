import datetime
import os
from flask import Blueprint, request
import json
import uuid
import jwt
from .. import jwtman

JWT_SECRET = os.environ['JWT_SECRET']

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api')

def error_return (message):
    return json.dumps({
        'success': False,
        'error': message,
	})

def check_jwt(encoded_jwt):
    id = jwtman.jwt_tok_validate(encoded_jwt)
    with open("flaskr/data/users.json", "r") as users_fp:
        users_db = json.load(users_fp)
        user_found = next((user for user in users_db if ((user['id'] == id))), False)
        return user_found

@checkout_bp.route('book/<id>/checkout_req', methods=['POST']) 
def request_checkout(id):
    data = request.json
    encoded_jwt = data.get('jwt')

    user = check_jwt(encoded_jwt)
    if not user:
        return error_return("Invalid jwt")

    with open("flaskr/data/books.json", "r") as f:
        books_db = json.load(f)
        for book in books_db:
            if book['id'] == id:

                with open("flaskr/data/records.json", "r") as records_fp:
                    records_db = json.load(records_fp)

                    for record_i, record in enumerate(records_db):
                        if record['id'] == book['status_record']:
                            if record['type'] == 'checked_out':
                                return 'Already checked out', 200
                            new_checkout_req = {
                                'id': str(uuid.uuid4()),
                                'book': id,
                                'user': user['username']
                            }
                            
                            return 'success', 200
                
    
    return error_return("Can not find book")

@checkout_bp.route('checkout_req/<id>/manage', methods=['POST']) #TODO JWT token
def manage_checkout(id):
    data = request.json
    state = data.get('state')
    if state not in {'approve', 'deny'}:
        return 'Invalid state', 300

    encoded_jwt = data.get('jwt')

    user = check_jwt(encoded_jwt)
    if not user:
        return error_return("Invalid jwt")

    with open("flaskr/data/books.json", "r") as books_fp:
        books_db = json.load(books_fp)
        for book in books_db:
            if book['id'] == id and book['owner'] == user['username']:

                with open("flaskr/data/records.json", "r+") as records_fp:
                    records_db = json.load(records_fp)
                    for record_i, record in enumerate(records_db):
                        if record['id'] == book['status_record']:
                            if record['type'] == 'checked_out':
                                return error_return('Book is already checked out')
                            records_db[record_i]['type'] = 'checked_out'
                            records_fp.seek(0)
                            records_fp.write(json.dumps(records_db))
                            return 'success', 200
                    return error_return('Can not find matching record id')

        return error_return('Can not find book id')
    
    return error_return('Error opening file')
