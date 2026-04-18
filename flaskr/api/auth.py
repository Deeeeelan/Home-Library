from flask import Blueprint, render_template, abort, request
import json
import hashlib
import jwt
import dotenv
import os
import datetime
from datetime import timezone
dotenv.load_dotenv()
JWT_SECRET = os.environ['JWT_SECRET']

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
	data = request.json
	
	username = data.get("username")
	password = data.get("password")
	pwhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
	
	print("username: ", username)
	print("password HASH: ", pwhash)
	
	with open("flaskr/data/users.json", "r") as users_fp:
		users_db = json.load(users_fp)
		user_found = next(user for user in users_db if ((user['username'] == username and user['pwhash'] == pwhash)))
		
		if user_found:
			now = datetime.datetime.now(tz=timezone.utc)
			generated_jwt = jwt.encode({
				'iat': now,
				'exp': now + datetime.timedelta(days=3),
				'sub': user_found['id'],
			}, JWT_SECRET, algorithm='HS256')
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

@auth_bp.route('/signup')
def signup():
	data = request.get_json()
	print(data)
	
	username = data["username"]
	password = data["password"]
	name = data["name"]
	# TODO: location
	
	print("username: ", username)
	
	return 'signup page!'
