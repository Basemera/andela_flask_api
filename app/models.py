from flask_sqlalchemy import SQLAlchemy
from app.app import api, app, db, session
from flask import abort, g, jsonify
#       from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'


#create the User model
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
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()  

    @staticmethod
    def get_all_users():
        return User.query.all()
    #method to hasg the password using passlib
    def hash_password(self, password):
        self.password = password
        self.password = pwd_context.encrypt(password)

    def verify_passwords(self, password):
        return pwd_context.verify(password, self.password)

    
    def generate_auth_token(self, expiration = 600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({ 'userid': self.userid })

    @auth.verify_password
    def verify_password(username_or_token, password):
    # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if user:
            #user = session.query(User).filter_by(userid = userid).one()
            g.user = user
            return True
            
        else:
        # try to authenticate with username/password
            user = session.query(User).filter_by(username = username_or_token).first()
            if not user or not user.verify_passwords(password):
                return False
            g.user = user
            return True
        

    #method to verify a tioken
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = data['userid']
        # user = User.query.get(data['userid'])
        return user

    
          
    
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
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()  

    @staticmethod
    def get_all_users():
        return RecipeCategory.query.all()

   
        
        

    
    def __repr__(self):
        return '<Category %r>' % (self.category_name)

#define a clas to hold the recipes
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
    

    def __repr__(self):
        return '<Category %r>' % (self.name)