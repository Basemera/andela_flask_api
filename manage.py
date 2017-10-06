#handle migrations
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import db
from app.app import app

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
@manager.command
def create_database(default_data = True, sample_data = False):
     db.create_all()

@manager.command
def drop_database():
     db.drop_all() 

if __name__ == '__main__':
    manager.run()