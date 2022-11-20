import os.path

from flask import Flask
import config
from apps.admin import bp as admin_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from exts import db


def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(admin_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.config.from_object(config)
    if os.path.exists('local.py'):
        import local

        app.config.from_object(local)
    app.secret_key = "super secret key"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app()
    is_debug_mode = app.config['DEBUG']
    app.run(debug=is_debug_mode)
