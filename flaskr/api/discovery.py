from flask import Blueprint, request
import json
from fuzzywuzzy import fuzz

discovery_bp = Blueprint('discovery', __name__, url_prefix='/api')

@discovery_bp.route('/user/<username>')
def user(username):

    with open("flaskr/data/users.json", "r") as f:
        user_database = json.load(f)
        print(user_database)
        for user in user_database:
            if user['username'] == username:
                user.pop("password")
                return user
    
    return 'Could not find user', 400

@discovery_bp.route('/search')
def search():
    data = request.json

    zip_code = data.get('zip_code')
    name = data.get('name')
    author = data.get('author')

    found = []

    with open("flaskr/data/books.json", "r") as f:
        book_database = json.load(f)
        for book in book_database:
            met_criteria = False
            if book['zip_code'] == zip_code:
                met_criteria = True
            if author and book['author'] != author:
                met_criteria = False
            
            if name:
                fuzzy_result = fuzz.ratio(name, book['name'])
                if fuzzy_result < 60:
                    met_criteria = False

            if met_criteria:
                found.append(book) 
    
    return found

