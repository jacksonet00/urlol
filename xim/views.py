from app import app, db
from flask import request, redirect
from models import User
import json
from utils import get_hashed_password


@app.route('/user/', methods=['GET', 'POST'])
@app.route('/user/<id>', methods=['GET'])
def user(id=None):
    if request.method == 'GET':
        if id:
            user = User.query.get(id)
            return json.dumps(user.as_dict())
        email = request.args.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            return json.dumps(user.as_dict())
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        _response = {
            'errors': [],
            'data': None,
        }

        if not email or not password:
            if not email:
                _response['errors'].append({
                    'message': 'Email is required.'
                })
            if not password:
                _response['errors'].append({
                    'message': 'Password is required.'
                })
            return json.dumps(_response)

        hashed_password = get_hashed_password(password)

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        _response['data'] = new_user.as_dict()

        return json.dumps(_response)


@app.route('/search')
def bunnylol():
    query = request.args.get('q')

    # github search
    if query[:3] == 'gh ':
        return redirect(f'https://github.com/search?q={query[3:]}')

    # wikipedia search
    if query[:2] == 'w ':
        return redirect(f'https://en.wikipedia.org/w/index.php?search={query[2:]}')

    # stack overflow search
    if query[:3] == 'so ':
        return redirect(f'https://stackoverflow.com/search?q={query[3:]}')

    # amazon search
    if query[:2] == 'a ':
        return redirect(f'https://www.amazon.com/s?k={query[2:]}')

    # fallback to google search by default
    return redirect(f'https://google.com/search?q={query}')
