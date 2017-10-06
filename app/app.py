from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from views import add_user


#from models import db
db = SQLAlchemy()


Session = sessionmaker()
engine = create_engine('postgresql://postgres:phiona@localhost:5432/myrecipes')
Session.configure(bind=engine)

# create a Session
session = Session()

#app config


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'phiona'
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:phiona@localhost:5432/myrecipes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    return app



app = create_app()
api = Api(app)
