from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login')
def login():
    data = request.get_json()
    print(data)
    
    username = data["username"]
    password = data["password"]
    
    print("username: ", username)
    
    return 'login page!'

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

# @auth_bp.route('/', defaults={'page': 'index'})
# @auth_bp.route('/<page>')
# def show(page):
#     try:
#         return render_template(f'pages/{page}.html')
#     except TemplateNotFound:
#         abort(404)