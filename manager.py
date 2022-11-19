# encoding:utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from exts import db
from apps.admin import models as admin_models

r'''
当数据库结构发生改变时，迁移数据库使用
在Flask的最新版本，貌似已经不支持这么做了..
'''

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_user(username, password, email):
    user = admin_models.Users(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print(f'用户添加成功: {user.username}')


if __name__ == '__main__':
    manager.run()
