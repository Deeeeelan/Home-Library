from flask import Blueprint, render_template, abort, request
import json
from fuzzywuzzy import fuzz

discovery_bp = Blueprint('discovery', __name__, url_prefix='/api')

@discovery_bp.route('/user/<username>')
def user(username):

    print("username: ", username)
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
    data = request.get_json()

    zip_code = data["zip_code"]
    name = data["name"] if 'name' in data else None
    author = data["author"] if 'author' in data else None

    found = []

    with open("flaskr/data/books.json", "r") as f:
        book_database = json.load(f)
        print(book_database)
        for book in book_database:
            met_criteria = False
            if book['zip_code'] == zip_code:
                met_criteria = True
            if author and book['author'] != author:
                met_criteria = False
            
            if name:
                fuzzy_result = fuzz.ratio(name, book['name'])
                print(fuzzy_result)
                if fuzzy_result < 60:
                    met_criteria = False

            if met_criteria:
                found.append(book) 
    
    return found

