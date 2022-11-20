# encoding:utf-8
from io import BytesIO

from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from .models import Users
from .forms import LoginForm
from utils.captcha import create_validate_code
from datetime import timedelta
from .decorators import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            captcha = request.form.get('captcha')
            if session.get('image').lower() != captcha.lower():
                return render_template('admin/login.html', message='验证码不符')

            # 记住登录状态
            online = request.form.get('online')
            if online:
                session.permanent = True
                bp.permanent_session_life_time = timedelta(days=14)

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
    # return render_template('admin/index.html')
    return '后台管理首页'


@bp.route('/test/')
@login_required
def test():
    return 'test index'


@bp.route('/code/')
def get_code():
    # 把strs发给前端，或者在后台使用session保存
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    # buf.seek(0)
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    # 将验证码字符串存储在session中
    session['image'] = strs
    return response
