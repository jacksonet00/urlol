from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..model.core import db

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    return render_template('dashboard/index.html')
