from app import app, db, login_manager
from flask import request, redirect
from models import User
import json
from flask_login import login_user, login_required, logout_user
from bcrypt import checkpw, hashpw, gensalt
import re


@app.route('/signup', methods=['POST'])
def sign_up():
    _response = {
        'errors': [],
        'data': None
    }

    if request.method != 'POST':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        return json.dumps(_response)

    email = request.json['email']
    password = request.json['password']

    if User.query.filter_by(email=email).first() != None:
        _response['errors'].append({
            'message': 'Email already in use.'
        })
        return json.dumps(_response)

    email_regex = re.compile('^.+@[a-zA-Z0-9]{2,}\\.[a-zA-Z]{2,}$')
    if not email_regex.match(email):
        _response['errors'].append({
            'message': 'Invalid email.'
        })

    password_regex = re.compile('^[a-zA-Z0-9!?!$*.]{5,50}$')
    if not password_regex.match(password):
        _response['errors'].append({
            'message': 'Invalid password.'
        })

    if _response['errors']:
        return json.dumps(_response)

    hashed_password = hashpw(password.encode('utf8'), gensalt()).decode('utf8')

    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    _response['data'] = new_user.as_dict()
    return json.dumps(_response)


@app.route('/login', methods=['POST'])
def login():
    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'POST':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        return json.dumps(_response)

    email = request.json['email']
    password = request.json['password']

    if not email:
        _response['errors'].append({
            'message': 'Email required.'
        })

    if not password:
        _response['errors'].append({
            'message': 'Password required.'
        })

    if _response['errors']:
        return json.dumps(_response)

    user = User.query.filter_by(email=email).first()
    if not user:
        _response['errors'].append({
            'message': f'No user associated {email}.'
        })
        return json.dumps(_response)

    if not checkpw(password.encode('utf8'), user.password.encode('utf8')):
        _response['errors'].append({
            'message': f'Incorrect password for {email}'
        })

    login_user(user)

    _response['data'] = user.as_dict()
    return json.dumps(_response)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out.'


@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user


@app.route('/user/')
@app.route('/user/<id>')
def user(id=None):
    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'GET':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        return json.dumps(_response)

    email = request.args.get('email')

    if id:
        user = User.query.get(id)
    elif email:
        user = User.query.filter_by(email=email).first()

    if not user:
        def lookup_method(): return 'user id' if id else 'email'
        _response['errors'].append({
            'message': f'Invalid {lookup_method()}.'
        })
        return json.dumps(_response)

    return json.dumps(user.as_dict())
