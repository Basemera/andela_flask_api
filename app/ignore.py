import os
#from os import urandom
from flask import g, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.declarative import declarative_base
#import random, String
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, 
    BadSignature, SignatureExpired)
from app import app
from app.app import db, api, auth, Session, app, create_app, session


# Base = declarative_base()
# secret_key = os.urandom(24)

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable=False, index = True)
    email = db.Column(db.String(100), unique = True, nullable = False, index = True)
    password = db.Column(db.String(128))
    #recipecategory = db.relationship('Recipe_Category', backref = 'User', lazy = 'dynamic')

    def __init__(self, userid, username, email, password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = password


    #function to add a user to the database
    def save_user(self):
        db.session.add(self)
        db.session.commit()
        # db.session.remove()
        # db.session.close()
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        db.session.remove()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({ 'userid': self.userid })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['userid'])
        return user

    @auth.verify_password
    def verify_password(username_or_token, password):
    # first try to authenticate by token
        #users = User.query.filter_by(username = username_or_token).first()
        userid = User.verify_auth_token(username_or_token)
        if userid:
            user = session.query(User).filter_by(userid = userid).one()
        else:
            user = session.query(User).filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
            g.user = user
            return True
        
        # if not user:
        # # try to authenticate with username/password
        #     user = User.query.filter_by(username = username_or_token).first()
        #     if not user or not user.verify_password(password):
        #         return False
        # g.user = user
        # return True

    #@app.route('/users/<int:userid>')
    def get(userid):
        user = User.query.get(userid)
        if not user:
            abort(400)
        return jsonify({'username': user.username})

    @app.route('/token')
    @auth.login_required
    def get_auth_token():
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration':600})

    

    # @auth.verify_password
    # def verify_password(username_or_token, password):
    # # first try to authenticate by token
    #     userid = User.verify_auth_token(username_or_token)
    #     if userid:
    #     # try to authenticate with username/password
    #         user = session.query(User).filter_by(userid = userid).one()
    #         g.user = user
    #         return True

    #         # if not user or not User.verify_password(username_or_token, password):
    #         #     return False
    #     else:
    #         user = session.query(User).filter_by(username = username_or_token).first()
    #         if not user or not user.verify_password(password):
    #             return False

    
        # g.user = user
        # return True

    

class RecipeCategory(db.Model):
    __tablename__ = 'recipe_category'
    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(200), index = True)
    #userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    #recipes = db.relationship('Recipes', backref = 'RecipeCategory', lazy = 'dynamic')

        #intialise the class
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        db.session.rollback()  

    @staticmethod
    def get_all_users():
        return RecipeCategory.query.all()


class Recipes(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column('recipe_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(250), nullable = False, index = True)
    userid = db.Column('userid', db.Integer, db.ForeignKey('user.userid'))
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('recipe_category.category_id'))

    def __init__(self, recipe_id, name):
        self.recipe_id = recipe_id
        self.name = name

    def save_user(self):
        db.session.add(self)
        db.session.commit()
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()  

    @staticmethod
    def get_all_users():
        return User.query.all()
    

    # def __repr__(self):
    #     return '<Category %r>' % (self.name)

