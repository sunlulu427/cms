# encoding:utf-8
from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Users
from .forms import LoginForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = request.form.get('username')
            password = request.form.get('password')
            users = Users.query.filter_by(username=user).first()
            if users:
                if user == users.username and users.check_password(password):
                    session['user_id'] = users.uid
                    print(f'用户id: {session["user_id"]}')
                    print('密码对!')
                    return redirect(url_for('admin.index'))
                else:
                    error = '用户名或密码错误！'
                    return render_template('admin/login.html', message=error)
            else:
                return render_template('admin/login.html', message='没有此用户')
        else:
            return render_template('admin/login.html', message=form.errors)

@bp.route('/')
def index():
    return render_template('admin/index.html')
