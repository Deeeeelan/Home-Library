import os
from flask import Blueprint, request
import json
import uuid
from .. import jwtman

JWT_SECRET = os.environ['JWT_SECRET']

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api')

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

@checkout_bp.route('book/<book_id>/checkout_req', methods=['POST']) 
def request_checkout(book_id):
	data = request.json
	encoded_jwt = data.get('jwt')

	user = check_jwt_data(encoded_jwt)
	if not user:
		return respond_error("Invalid jwt")

	with open("flaskr/data/books.json", "r") as f:
		books_db = json.load(f)
		
		book_found = next((book for book in books_db if (book['id'] == book_id)), None)
		if book_found:

			with open("flaskr/data/records.json", "r") as records_fp:
				records_db = json.load(records_fp)
				
				record_found = next((record for record in records_db if (record['id'] == book_found['status_record'])), None)
				if record_found:
					if record_found['type'] == 'checked_out':
						return respond_error("Book already checked out"), 200
					
					new_checkout_req = {
						'id': str(uuid.uuid4()),
						'book': book_id,
						'user': user['id'],
					}
					
					# open checkreg file and add record
					with open("flaskr/data/checkout_reg.json", "r+") as checkreg_fp:
						checkreg_db = json.load(checkreg_fp)
						checkreg_db.append(new_checkout_req)
						checkreg_fp.seek(0)
						checkreg_fp.write(json.dumps(checkreg_db))
						checkreg_fp.truncate()
						return respond_success(), 200
					
				else:
					return respond_error("Book data malformed, our fault!"), 500
		else:
			return respond_error("Book doesn't exist")
			
	

@checkout_bp.route('checkout_req/<id>/manage', methods=['POST'])
def manage_checkout(id):
	data = request.json
	state = data.get('state')
	if state not in {'approve', 'deny'}:
		return respond_error('Invalid state'), 400

	encoded_jwt = data.get('jwt')

	user = check_jwt_data(encoded_jwt)
	if not user:
		return respond_error("Invalid jwt"), 400

	with open("flaskr/data/checkout_reg.json", "r+") as checkregs_fp:
		checkregs_db = json.load(checkregs_fp)
		checkreg_found = next((checkreg for checkreg in checkregs_db if (checkreg['id'] == id)), None)
		
		if not checkreg_found:
			return respond_error("That checkout request doesn't exist."), 400
		
		book_id = checkreg_found['book']
		
		if state == 'deny':
			checkregs_db = [checkreg for checkreg in checkregs_db if checkreg['id'] != id]
			checkregs_fp.seek(0)
			checkregs_fp.write(json.dumps(checkregs_db))
			checkregs_fp.truncate()
			return respond_success(), 200
		else: # state == 'approve'
			checkregs_db = [checkreg for checkreg in checkregs_db if checkreg['book'] != book_id]
			checkregs_fp.seek(0)
			checkregs_fp.write(json.dumps(checkregs_db))
			checkregs_fp.truncate()
			
			new_record_id = str(uuid.uuid4())
			with open("flaskr/data/records.json", "r+") as records_fp:
				records_db = json.load(records_fp)
				records_db.append({
					'id': new_record_id,
					'type': 'checked_out',
					'book': book_id,
					'user': checkreg_found['user'],
				})
				records_fp.seek(0)
				records_fp.write(json.dumps(records_db))
				records_fp.truncate()
			
			with open("flaskr/data/books.json", "r+") as books_fp:
				books_db = json.load(books_fp)
				for book_i, book in enumerate(books_db):
					if book['id'] == book_id:
						books_db[book_i]['status_record'] = new_record_id
				books_fp.seek(0)
				books_fp.write(json.dumps(books_db))
				books_fp.truncate()
			
			return respond_success(), 200
	
	return respond_error('Error opening file'), 400
