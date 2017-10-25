from flask import Flask, render_template, request, jsonify, g, json, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource
from app import app
from app.app import db, app, api, auth, session
from app.models import *

class Token(Resource):
    @auth.login_required
    def get():
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')}) 


#object to create users
class AddUser(Resource):
    def post(self):  
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type = int)
        parser.add_argument('username', type = str)
        parser.add_argument('email', type = str)
        parser.add_argument('password', type = str)
        args = parser.parse_args()
        userid = args['userid']
        username = args['username']
        email = args['email']
        password = args['password']
        person = User.query.filter_by(username = username).first()
        email = User.query.filter_by(email = email).first()
        if person is None:
            new_user = User(userid, username, email, password)
            new_user.hash_password(password)
            new_user.save_user()
            return jsonify({'userid': args['userid'],'Username': args['username'],'Email': args['email'], 'Password': args['password']})
        else:
            return ({"message": "User already exists"})

    @auth.login_required
    def get(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type = int)
        parser.add_argument('username', type = str)
        parser.add_argument('email', type = str)
        args = parser.parse_args()
        userid = args['userid']
        username = args['username']
        email = args['email']
        user = User.query.filter_by(userid = userid).first()
        if user is None:
            return ({'message': 'User doesnot exist'})
        return ({'userid':user.userid})

        
        

class Addrecipe_category(Resource):
    @auth.login_required
    def post(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('category_id', type = int)
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        category_id = args['category_id']
        category_name = args['category_name']
        category = RecipeCategory.query.filter_by(category_name = category_name).first()
        #user = token
        # if user is None:
        #     return ({"message": "you are not logged in"})
        #else:
        if category is None:
            new_category = RecipeCategory(category_id, category_name)
            new_category.save_user()
                #response = jsonify({'message': "Recipe category successfully created"})
                #return response
            return ({'message': "Recipe created"})
        
        else:
            response = ({'message': "Recipe already exists"})
            return response

    
    @auth.login_required
    def get(self, category_name):
        response = RecipeCategory.query.filter_by(category_name = category_name).first()
        if response is None:
            return jsonify({'message': 'category doesnot exist'})
        category = RecipeCategory.query.filter_by(category_name = category_name)
       # cat_id = RecipeCategory.query.filter_by(category_name = category_name)
        return jsonify({'category_name': category_name})
        #return jsonify({'username': 'category exists'})

class editcategory(Resource):
    '''function to update records'''
    @auth.login_required
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        category_name = args['category_name']
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'})
        cat.category_name = category_name
        db.session.commit()
        return ({'category name':cat.category_name, 'category_id':category_id})
        
        
class deletecategory(Resource):
    @auth.login_required
    def delete(self, category_id):
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'})
        # category_name = cat.category_name
        # cats = RecipeCategory(category_id, category_name)
        db.session.delete(cat)
        db.session.commit()
        
        return ({'message':'successfully deleted'})

class Addrecipe(Resource):
    @auth.login_required
    def post(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_id', type = int)
        parser.add_argument('name', type = str)
        args = parser.parse_args()
        recipe_id = args['recipe_id']
        name = args['name']
        recipe = Recipes.query.filter_by(name = 'name').first()
        #ids = Recipes.query.filter_by(recipe_id = 'recipe_id').first()
        if recipe is None:
            new_recipe = Recipes(recipe_id, name)
            new_recipe.save_user()
            response = jsonify({'message': 'recipe successfully added', 'recipeid':recipe_id})
            return response
            #return jsonify({'category_id': args['category_id'],'category_name': args['category_name']})
        else:
            #if recipe is not None:
            return ({"message": "Recipe already exists"})





class Login(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type = str)
        parser.add_argument('password', type = str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        #user = User.query.filter_by(username = username).first()
        users = User.query.filter_by(username = username).first()
        if users and password:
            
           
            user = User.verify_password(username, password)
            
            if user:
                token = g.user.generate_auth_token()
                user = g.user
                return jsonify({ 'token': token.decode('ascii') })
            else:
                return ({"message": "you are not signed up"})
                
        else:
            return ({"message": "you must provide both a password and a username"})


    # @auth.login_required
    # def get():
    #     token = g.user.generate_auth_token()
    #     return jsonify({'token': token.decode('ascii')})

        
        