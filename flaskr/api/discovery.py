from flask import Blueprint, request
import json
from fuzzywuzzy import fuzz

discovery_bp = Blueprint('discovery', __name__, url_prefix='/api')

def respond_error (message):
	return json.dumps({
		'success': False,
		'error': message,
	})

@discovery_bp.route('/user/<username>', methods=['GET'])
def user(username):

	with open("flaskr/data/users.json", "r") as f:
		users_db = json.load(f)
		print(users_db)
		user_found = next((user for user in users_db if (user['username'] == username)), None)
		user_found.pop('pwhash')
		return json.dumps({
			'success': True,
			'user': user,
		})
	
	return respond_error('Could not find user'), 400

@discovery_bp.route('/search', methods=['GET'])
def search():
	zip_code = request.args.get('zip_code')
	name = request.args.get('name')
	author = request.args.get('author')

	found = []

	with open("flaskr/data/books.json", "r") as f:
		book_database = json.load(f)
		for book in book_database:
			met_criteria = False
			if book['zip_code'] == zip_code:
				met_criteria = True
			
			if author:
				fuzzy_result = fuzz.ratio(author, book['author'])
				if fuzzy_result < 60:
					met_criteria = False
			
			if name:
				fuzzy_result = fuzz.ratio(name, book['name'])
				if fuzzy_result < 60:
					met_criteria = False

			if met_criteria:
				found.append(book) 
	
	return json.dumps({
		'success': True,
		'books': found,
	})

