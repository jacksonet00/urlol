from ..model import User
from ..model.core import db

import re
import functools
from datetime import timedelta

from flask import Blueprint, request, render_template, redirect, url_for, session, g
from bcrypt import hashpw, gensalt, checkpw


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        g.user = user


@bp.route('/register', methods=('GET', 'POST'))
def register():
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
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
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

        session['user_id'] = user.id

        return redirect(url_for('index'))
    return render_template('auth/login.html')


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))
