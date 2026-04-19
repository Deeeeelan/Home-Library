from flask import Blueprint, render_template, abort, request
import json
import hashlib
import uuid
from ..jwtman import jwt_tok_generate, jwt_tok_validate

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
	data = request.json
	
	username = data.get('username')
	password = data.get('password')
	pwhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
	
	with open('flaskr/data/users.json', 'r') as users_fp:
		users_db = json.load(users_fp)
		user_found = next((user for user in users_db if ((user['username'] == username and user['pwhash'] == pwhash))), False)
		
		if user_found:
			generated_jwt = jwt_tok_generate(user_found['id'])
			return json.dumps({
				'success': True,
				'jwt': generated_jwt,
			})
		else:
			return json.dumps({
				'success': False,
				'jwt': None,
			})
	
	return json.dumps({
		'success': False,
		'jwt': None,
	})

@auth_bp.route('/signup', methods=['POST'])
def signup():
	data = request.json
	
	username = data.get('username')
	password = data.get('password')
	display_name = data.get('display_name')
	zip_code = data.get('zip_code')
	pwhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
	
	with open('flaskr/data/users.json', 'r+') as users_fp:
		users_db = json.load(users_fp)
		user_found = next((user for user in users_db if (user['username'] == username)), False)
		
		if user_found:
			return json.dumps({
				'success': False,
				'error': 'Username already used.'
			})
		else:
			users_db.append({
				'id': str(uuid.uuid4()),
				'username': username,
				'pwhash': pwhash,
				'display_name': display_name,
				'zip_code': zip_code,
				'books': [],
			})
			users_fp.seek(0)
			users_fp.write(json.dumps(users_db))
			users_fp.truncate()
			return json.dumps({
				'success': True,
				'error': None,
			})
	
	return json.dumps({
		'success': False,
		'error': None,
	})
