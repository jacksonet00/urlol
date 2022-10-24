from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from .auth import login_required
from ..model.core import db

bp = Blueprint('search', __name__)


@bp.route('/search', methods=['GET'])
@login_required
def search():
    if request.method == 'GET':
        errors = []

        if 'q' not in request.args:
            errors.append({
                'message': 'Query must be provided in `/search?q={query}`.'
            })
            return render_template('error.html', errors=errors)

        query = request.args['q']

        aliases = {
            alias.name: alias.url for alias in g.user.aliases} if g.user.aliases else {}

        if query in aliases:
            return redirect(aliases[query])

        return redirect(f'https://google.com/search?q={query}')
