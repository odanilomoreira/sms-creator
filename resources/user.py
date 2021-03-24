from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank.")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
atributos.add_argument('username', type=str)
atributos.add_argument('activated', type=bool)

class User(Resource):
    # /users/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /register
    def post(self):
        data = atributos.parse_args()
        if not data.get('email') or data.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "The email '{}' already exists.".format(data['email'])}, 400

        if UserModel.find_by_username(data['username']):
            return {"message": "The username '{}' already exists.".format(data['username'])}, 400 #Bad Request

        user = UserModel(**data)
        user.activated = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201 # Created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = atributos.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            if user.activated:
                access_token = create_access_token(identity=user.user_id)
                return {'access_token': access_token}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The email or password is incorrect.'}, 401 # Unauthorized


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200

class UserConfirm(Resource):
    # /confirm/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User id '{}' not found.".format(user_id)}, 404

        user.activated = True
        user.save_user()
        # return {"message": "User id '{}' confirmed successfully.".format(user_id)}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, user=user.username), 200, headers)
