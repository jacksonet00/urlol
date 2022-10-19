from app import app, db, login_manager
from flask import request, redirect, Response, render_template
from models import User, Alias, Shortcut
import json
from flask_login import login_user, login_required, logout_user
from bcrypt import checkpw, hashpw, gensalt
from datetime import timedelta
import re


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/signup', methods=['POST'])
def sign_up():
    response = Response()

    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'POST':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        response.set_data(json.dumps(_response))
        return response

    if 'email' not in request.json:
        _response['errors'].append({
            'message': 'Email required.'
        })

    if 'password' not in request.json:
        _response['errors'].append({
            'message': 'Password required.'
        })

    if _response['errors']:
        response.set_data(json.dumps(_response))
        return response

    email = request.json['email']
    password = request.json['password']

    if User.query.filter_by(email=email).first() != None:
        _response['errors'].append({
            'message': 'Email already in use.'
        })
        response.set_data(json.dumps(_response))
        return response

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
        response.set_data(json.dumps(_response))
        return response

    hashed_password = hashpw(password.encode('utf8'), gensalt()).decode('utf8')

    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    from datetime import timedelta

    login_user(new_user, remember=True, duration=timedelta(days=365))
    # response.set_cookie('urlol-uid', new_user.id)

    _response['data'] = new_user.as_dict()
    response.set_data(json.dumps(_response))
    return response


@app.route('/login', methods=['POST'])
def login():
    response = Response()

    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'POST':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        response.set_data(json.dumps(_response))
        return response

    if 'email' not in request.json:
        _response['errors'].append({
            'message': 'Email required.'
        })

    if 'password' not in request.json:
        _response['errors'].append({
            'message': 'Password required.'
        })

    if _response['errors']:
        response.set_data(json.dumps(_response))
        return response

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        _response['errors'].append({
            'message': f'No user associated {email}.'
        })
        response.set_data(json.dumps(_response))
        return response

    if not checkpw(password.encode('utf8'), user.password.encode('utf8')):
        _response['errors'].append({
            'message': f'Incorrect password for {email}'
        })
        response.set_data(json.dumps(_response))
        return response

    login_user(user, remember=True, duration=timedelta(days=365))
    # response.set_cookie('urlol-uid', user.id)

    _response['data'] = user.as_dict()
    response.set_data(json.dumps(_response))
    return response


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    response = Response()

    logout_user()

    # response.set_cookie('urlol-uid', "")
    response.set_data(json.dumps({
        'errors': [],
        'data': {
            'success': True
        }
    }))
    return response


@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user


@app.route('/user/', methods=['GET'])
@app.route('/user/<id>', methods=['GET'])
def user(id=None):
    response = Response()

    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'GET':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        response.set_data(json.dumps(_response))
        return response

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
        response.set_data(json.dumps(_response))
        return response

    _response['data'] = user.as_dict()
    response.set_data(json.dumps(_response))
    return response


@app.route('/alias', methods=['GET', 'POST'])
@app.route('/alias/<id>', methods=['GET'])
@login_required
def alias(id=None):
    response = Response()

    _response = {
        'errors': [],
        'data': []
    }

    if request.method == 'POST':
        if 'user_id' not in request.json:
            _response['errors'].append({
                'message': 'Missing user_id. Must provide body={ user_id }.'
            })

        if 'name' not in request.json:
            _response['errors'].append({
                'message': 'Missing name. Must provide body={ name }.'
            })

        if 'url' not in request.json:
            _response['errors'].append({
                'message': 'Missing url. Must provide body={ url }.'
            })

        if _response['errors']:
            response.set_data(json.dumps(_response))
            return response

        user_id = request.json['user_id']
        name = request.json['name']
        url = request.json['url']

        # if user_id != request.cookies.get('urlol-uid'):
        # _response['errors'].append({
        #     'message': 'The provided `user_id` does not match the id of the authenticated user.'
        # })
        # response.set_data(json.dumps(_response))
        # return response

        new_alias = Alias(name=name, url=url, user_id=user_id)

        db.session.add(new_alias)
        db.session.commit()

        _response['data'] = new_alias.as_dict()
        response.set_data(json.dumps(_response))
        return response

    if request.method == 'GET':
        if id:
            alias = Alias.query.get(id)

            if not alias:
                _response['errors'].append({
                    'message': 'Invalid alias id.'
                })
                response.set_data(json.dumps(_response))
                return response

            _response['data'] = alias.as_dict()
            response.set_data(json.dumps(_response))
            return response

        if 'user_id' not in request.json:
            _response['errors'].append({
                'message': 'Invalid HTTP request. Provide body: { user_id } for Alias[] or `/alias/<alias_id>` for Alias.'
            })
            response.set_data(json.dumps(_response))
            return response

        user_id = request.json['user_id']

        aliases = Alias.query.filter_by(user_id=user_id)

        _response['data'] = [alias.as_dict() for alias in aliases]
        response.set_data(json.dumps(_response))
        return response

    _response['errors'].append({
        'message': 'Invalid HTTP method.'
    })
    response.set_data(json.dumps(_response))
    return response


@app.route('/shortcut', methods=['GET', 'POST'])
@app.route('/shortcut/<id>', methods=['GET'])
@login_required
def shortcut(id=None):
    response = Response()

    _response = {
        'errors': [],
        'data': []
    }

    if request.method == 'POST':
        if 'user_id' not in request.json:
            _response['errors'].append({
                'message': 'Missing user_id. Must provide body={ user_id }.'
            })

        if 'prefix' not in request.json:
            _response['errors'].append({
                'message': 'Missing prefix. Must provide body={ prefix }.'
            })

        if 'website' not in request.json:
            _response['errors'].append({
                'message': 'Missing website. Must provide body={ website }.'
            })

        if _response['errors']:
            response.set_data(json.dumps(_response))
        return response

        user_id = request.json['user_id']
        prefix = request.json['prefix']
        website = request.json['website']

        # if user_id != request.cookies.get('urlol-uid'):
        #     _response['errors'].append({
        #         'message': 'The provided `user_id` does not match the id of the authenticated user.'
        #     })
        #     response.set_data(json.dumps(_response))
        # return response

        new_shortcut = Shortcut(
            prefix=prefix, website=website, user_id=user_id)

        db.session.add(new_shortcut)
        db.session.commit()

        _response['data'] = new_shortcut.as_dict()
        response.set_data(json.dumps(_response))
        return response

    if request.method == 'GET':
        if id:
            shortcut = Shortcut.query.get(id)

            if not shortcut:
                _response['errors'].append({
                    'message': 'Invalid shortcut id.'
                })
                response.set_data(json.dumps(_response))
                return response

            _response['data'] = shortcut.as_dict()
            response.set_data(json.dumps(_response))
            return response

        if 'user_id' not in request.json:
            _response['errors'].append({
                'message': 'Invalid HTTP request. Provide body: { user_id } for shortcut[] or `/shortcut/<shortcut_id>` for shortcut.'
            })
            response.set_data(json.dumps(_response))
            return response

        user_id = request.json['user_id']

        shortcuts = Shortcut.query.filter_by(user_id=user_id)

        _response['data'] = [shortcut.as_dict() for shortcut in shortcuts]
        response.set_data(json.dumps(_response))
        return response

    _response['errors'].append({
        'message': 'Invalid HTTP method.'
    })
    response.set_data(json.dumps(_response))
    return response


@app.route('/search', methods=['GET'])
@login_required
def search():
    response = Response()
    _response = {
        'errors': [],
        'data': []
    }

    if request.method != 'GET':
        _response['errors'].append({
            'message': 'Invalid HTTP method.'
        })
        response.set_data(json.dumps(_response))
        return response

    if 'q' not in request.args:
        _response['errors'].append({
            'message': 'Query string must be provided in `/search?q={query}&uid={user_id}`.'
        })

    if 'uid' not in request.args:
        _response['errors'].append({
            'message': 'User id must be provided in `/search?q={query}&uid={user_id}`.'
        })

    if _response['errors']:
        response.set_data(json.dumps(_response))
        return response

    query = request.args.get('q')

    user_id = request.args.get('uid')
    user = User.query.get(user_id)

    if not user:
        _response['errors'].append({
            f'message': 'Unable to fetch user with user_id={user_id} from the database.'
        })
        response.set_data(json.dumps(_response))
        return response

    if not user.is_authenticated:
        _response['errors'].append({
            f'message': 'User not authenticated, please login.'
        })
        response.set_data(json.dumps(_response))
        return response

    aliases = {
        alias.name: alias.url for alias in user.aliases} if user.aliases else {}

    if query in aliases:
        return redirect(aliases[query])

    return redirect(f'https://google.com/search?q={query}')


# TEST


@app.route('/auth')
@login_required
def auth():
    return 'success.'
