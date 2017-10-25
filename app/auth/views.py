from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_restful import reqparse, Resource
from app import app
from app.app import db, app, Bcrypt
from app.models import User

auth_blueprint = Blueprint('auth', __name__)

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
        encrypted_p = Bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        person = User.query.filter_by(username = username).first()
        email = User.query.filter_by(email = email).first()
        if person is None:
            new_user = User(userid, username, email, encrypted_p)
            #new_user.hash_password(password)
            new_user.save_user()
            auth_token = new_user.encode_auth_token(username)
            responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()}

            return ({"message": "registered"})
            #return make_response(jsonify(responseObject)), 201

        
        # else:
        #     responseObject = {
        #             'status': 'fail',
        #             'message': 'Some error occurred. Please try again.'
        #         }
        #     return make_response(jsonify(responseObject)), 401
        
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return ({"message": "not registered"})
            #return make_response(jsonify(responseObject)), 202

           