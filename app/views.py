from flask import Flask, render_template, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource
from app.app import db, app, api
from app.models import User, session, auth, g, RecipeCategory

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
        if person is None:
            new_user = User(userid, username, email, password)
            new_user.hash_password(password)
            new_user.save_user()
            return jsonify({'userid': args['userid'],'Username': args['username'],'Email': args['email'], 'Password': args['password']})
        else:
            return ({"message": "User already exists"})

    def get(self):
        return ({"message": "User already exists"})
#@app.route('/login')
#@auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({ 'token': token.decode('ascii') })
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type = str)
        parser.add_argument('password', type = str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if username and password:
            user = User.query.filter_by(username = username).first()
            user = User.verify_password(username, password) 
        else:
            return ({"message": "you must provide both a password and a username"})

        
        if user:
            token = g.user.generate_auth_token()
            return jsonify({ 'token': token.decode('ascii') })
        else:
            return ({"message": "you are not signed up"})
#login
#class Login(Resource):
    
    #request token
    #@auth.login_required
    # def post(self):
    #     token = g.user.generate_auth_token()
    #     return jsonify({ 'token': token.decode('ascii') })
    # 
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
        user = g.user
        if user is None:
            return ({"message": "you are not logged in"})
        else:
            if category is None:
                new_category = RecipeCategory(category_id, category_name)
                new_category.save_user()
                #response = jsonify({'message': "Recipe category successfully created"})
                #return response
                return ({'message': "Recipe created"})
        #({'category_id': category_id,'category_name': category_name})
            else:
                response = ({'message': "Recipe already exists"})
                return response

    # def get(self):
    #     response = RecipeCategory.get_all_users()
    #     return ({'category_name':"category_name"})

    # def post(category_id):
    #     response = RecipeCategory.query.filter_by(category_id = "category_id")
        
    #     return ({'category_'})

class Addrecipe(Resource):
    @auth.login_required
    def post(self): 
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_id', type = int)
        parser.add_argument('name', type = str)
        args = parser.parse_args()
        _Recipesrecipe_id = args['recipe_id']
        _Recipesname = args['name']
        recipe = Recipes.query.filter_by(name = 'name').first()
        if recipe is None:
            new_recipe = Recipes(_Recipesrecipe_id, _Recipesname)
            new_recipe.save_user()
            respone = jsonify({'message': 'recipe successfully added'})
            #return jsonify({'category_id': args['category_id'],'category_name': args['category_name']})
        else:
            return ({"message": "Recipe already exists"})
