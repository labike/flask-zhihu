# encoding: utf-8

from index import app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from models import User

manage = Manager(app)

# bind app and db
migrate = Migrate(app, db)

# migrate db
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()