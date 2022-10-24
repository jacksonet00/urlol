from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from ..model.core import db
from ..model import Alias

bp = Blueprint('alias', __name__)


@bp.route('/alias', methods=['POST'])
@login_required
def create_alias():
    new_alias = Alias(
        name=request.form['name'], url=request.form['url'], user_id=g.user.id)
    db.session.add(new_alias)
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/alias/update', methods=['POST'])
@login_required
def update_alias():
    alias = Alias.query.get(request.form['id'])
    if request.form['name']:
        alias.name = request.form['name']
    if request.form['url']:
        alias.url = request.form['url']
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/alias/delete', methods=['POST'])
@login_required
def delete_alias():
    alias = Alias.query.get(request.form['id'])
    db.session.delete(alias)
    db.session.commit()

    return redirect(url_for('index'))
