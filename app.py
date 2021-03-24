from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from blacklist import BLACKLIST
from flask_cors import CORS

# webhook_url = 'https://webhook.site/a7e52c0d-532a-48e8-adc9-faecebee02c7'
# secret_key = '40d6f141-fe3b-4f9d-824a-f04084762d31' #Restaurant ID

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def hello():
    return '<h1>Up and running...</h1>'

@app.before_first_request
def create_database():
    db.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_tokens(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401 # unauthorized

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserConfirm, '/confirm/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)