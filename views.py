from app import app, db, login_manager
from models import User, Alias, Shortcut

import json
import re
from datetime import timedelta

from flask import request, redirect, render_template, url_for
from flask.sessions import SecureCookieSessionInterface
from flask_login import login_user, logout_user
from bcrypt import checkpw, hashpw, gensalt


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        session_interface = SecureCookieSessionInterface()
        signing_serializer = session_interface.get_signing_serializer(app)

        if 'session' in request.cookies:
            session_cookie = request.cookies.get('session')
            session_cookie_data = signing_serializer.loads(session_cookie)

            if '_user_id' in session_cookie_data:
                user_id = session_cookie_data['_user_id']
                user = User.query.get(user_id)

                if user:
                    return render_template('index.html', user=user)

        return render_template('index.html', user=None)


@app.route('/signup', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        errors = []

        if 'email' not in request.form:
            errors.append({
                'message': 'Email required.'
            })

        if 'password' not in request.form:
            errors.append({
                'message': 'Password required.'
            })

        if errors:
            return render_template('error.html', errors=errors)

        email = request.form['email'].lower()
        password = request.form['password']

        if User.query.filter_by(email=email).first() != None:
            errors.append({
                'message': 'Email already in use.'
            })
            return render_template('error.html', errors=errors)

        email_regex = re.compile('^.+@[a-zA-Z0-9]{2,}\\.[a-zA-Z]{2,}$')
        if not email_regex.match(email):
            errors.append({
                'message': 'Invalid email.'
            })

        password_regex = re.compile('^[a-zA-Z0-9!?!$*.]{5,50}$')
        if not password_regex.match(password):
            errors.append({
                'message': 'Invalid password.'
            })

        if errors:
            return render_template('error.html', errors=errors)

        hashed_password = hashpw(password.encode(
            'utf8'), gensalt()).decode('utf8')

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True, duration=timedelta(days=365))

        return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        errors = []

        if 'email' not in request.form:
            errors.append({
                'message': 'Email required.'
            })

        if 'password' not in request.form:
            errors.append({
                'message': 'Password required.'
            })

        if errors:
            return render_template('error.html', errors=errors)

        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            errors.append({
                'message': f'No user associated with {email}.'
            })
            return render_template('error.html', errors=errors)

        if not checkpw(password.encode('utf8'), user.password.encode('utf8')):
            errors.append({
                'message': f'Incorrect password for {email}.'
            })
            return render_template('error.html', errors=errors)

        login_user(user, remember=True, duration=timedelta(days=365))

        return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session_interface = SecureCookieSessionInterface()
        signing_serializer = session_interface.get_signing_serializer(app)

        if 'session' in request.cookies:
            session_cookie = request.cookies.get('session')
            session_cookie_data = signing_serializer.loads(session_cookie)

            if '_user_id' in session_cookie_data:
                user_id = session_cookie_data['_user_id']
                user = User.query.get(user_id)

                if user:
                    logout_user()
                    return redirect(url_for('index'))
        return redirect(url_for('index'))


@app.route('/alias', methods=['POST', 'GET'])
def alias(id=None):
    if request.method == 'POST':
        errors = []

        session_interface = SecureCookieSessionInterface()
        signing_serializer = session_interface.get_signing_serializer(app)

        if 'session' not in request.cookies:
            errors.append({
                'message': 'Authenticated session cookie not found.'
            })
            return render_template('error.html', errors=errors)

        session_cookie = request.cookies.get('session')
        session_cookie_data = signing_serializer.loads(session_cookie)

        if '_user_id' not in session_cookie_data:
            errors.append({
                'message': 'User id not stored in session cookie.'
            })
            return render_template('error.html', errors=errors)

        user_id = session_cookie_data['_user_id']
        user = User.query.get(user_id)

        if not user:
            errors.append({
                'message': f'User with id={user_id} not found.'
            })
            return render_template('error.html', errors=errors)

        if 'id' in request.form:  # DELETE by ID
            alias_id = request.form['id']
            alias = Alias.query.get(alias_id)

            if not alias:
                errors.append({
                    'message': f'Alias with id={alias_id} not found.'
                })
                return render_template('error.html', errors=errors)

            db.session.delete(alias)
            db.session.commit()

            return redirect(url_for('index'))

        else:  # CREATE (name, url)
            if 'name' not in request.form:
                errors.append({
                    'message': 'Name required.'
                })

            if 'url' not in request.form:
                errors.append({
                    'message': 'Url required.'
                })

            if errors:
                return render_template('error.html', errors=errors)

            name = request.form['name']
            url = request.form['url']

            session_interface = SecureCookieSessionInterface()
            signing_serializer = session_interface.get_signing_serializer(app)

            session_cookie = request.cookies.get('session')
            session_cookie_data = signing_serializer.loads(session_cookie)

            user_id = session_cookie_data['_user_id']

            new_alias = new_alias = Alias(name=name, url=url, user_id=user_id)

            db.session.add(new_alias)
            db.session.commit()

            return redirect(url_for('index'))

    if request.method == 'GET':  # UPDATE (name?, url?) by id
        errors = []

        if 'id' not in request.args:
            errors.append({
                'message': 'Alias id required.'
            })
            return render_template('error.html', errors=errros)

        id = request.args['id']
        alias = Alias.query.get(id)

        if not alias:
            errors.append({
                'message': f'Alias with id={id} not found.'
            })
            return render_template('error.html', errors=errors)

        if 'name' in request.args:
            name = request.args['name']
            alias.name = name

        if 'url' in request.args:
            url = request.args['url']
            alias.url = url

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        errors = []

        if 'q' not in request.args:
            errors.append({
                'message': 'Query must be provided in `/search?q={query}`.'
            })

        if 'session' not in request.cookies:
            errors.append({
                'message': 'Authenticated session cookie not found.'
            })

        if errors:
            return render_template('error.html', errors=errors)

        session_interface = SecureCookieSessionInterface()
        signing_serializer = session_interface.get_signing_serializer(app)

        session_cookie = request.cookies['session']
        session_cookie_data = signing_serializer.loads(session_cookie)

        query = request.args['q']

        user_id = session_cookie_data['_user_id']
        user = User.query.get(user_id)

        if not user:
            errors.append({
                'message': f'User with id={user_id} not found.'
            })
            return render_template('error.html', errors=errors)

        if not user.is_authenticated:
            errors.append({
                'message': 'User not authenticated.'
            })
            return render_template('error.html', errors=errors)

        aliases = {
            alias.name: alias.url for alias in user.aliases} if user.aliases else {}

        if query in aliases:
            return redirect(aliases[query])

        return redirect(f'https://google.com/search?q={query}')
