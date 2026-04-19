import datetime
import os
from flask import Blueprint, request
import json
import uuid
import jwt

JWT_SECRET = os.environ['JWT_SECRET']

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api')

@checkout_bp.route('book/<id>/checkout_req', methods=['POST']) 
def request_checkout(id):
    data = request.json
    encoded_jwt = data.get('jwt')
    try:
        decoded = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        return "invalid sig"
    except jwt.InvalidTokenError:
        return "invalid token"
    now = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    print(decoded['iat'])
    with open("flaskr/data/users.json", "r") as users_fp:
        users_db = json.load(users_fp)
        for user in users_db:
            if decoded['sub'] == user['id']:
                current_user = user
                print(current_user)        
    
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
                                'user':'user' # TODO
                            }
                            
                            return 'success', 200
                
    
    return 'test', 400

@checkout_bp.route('checkout_req/<id>/manage', methods=['POST']) #TODO JWT token
def manage_checkout(id):
    data = request.json
    state = data.get('state')
    if state not in {'approve', 'deny'}:
        return 'Invalid state', 300

    with open("flaskr/data/books.json", "r") as books_fp:
        books_db = json.load(books_fp)
        for book in books_db:
            if book['id'] == id:
                # TODO: check book owner

                with open("flaskr/data/records.json", "r+") as records_fp:
                    records_db = json.load(records_fp)
                    for record_i, record in enumerate(records_db):
                        if record['id'] == book['status_record']:
                            records_db[record_i]['type'] = 'checked_out'
                            records_fp.seek(0)
                            records_fp.write(json.dumps(records_db))
                            return 'success', 200
                    return 'Can not find matching record id', 400

        return 'Can not find book id', 400
    
    return 'Error opening file', 400
