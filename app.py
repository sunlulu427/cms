import os.path

from flask import Flask
import config
from apps.admin import bp as admin_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(admin_bp)
app.register_blueprint(common_bp)
app.register_blueprint(front_bp)

app.config.from_object(config)
if os.path.exists('local.py'):
    import local

    app.config.from_object(local)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    is_debug_mode = app.config['DEBUG']
    app.run(debug=is_debug_mode)
