# encoding:utf-8
from flask import Blueprint, render_template

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def index():
    return render_template('admin/login.html')
