import os.path

from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)
if os.path.exists('local.py'):
    import local

    app.config.from_object(local)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
