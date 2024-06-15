from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import request, jsonify, make_response

auth_ns=Namespace('auth', description="A namespace for authentication")


signup_model=auth_ns.model("SignUp", {
    "username": fields.String(),
    "email": fields.String(),
    "password": fields.String(),
})

login_model=auth_ns.model("Login", {
    "username": fields.String(),
    "password": fields.String(),
})


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data=request.get_json()
        username = data.get('username')
        db_user=self.check_user(username)
        if db_user is not None:
            return jsonify({"message": f"User with username {username} already exists"})
        
        new_user=User(
            username=username,
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
        )
        
        new_user.save()
        return make_response(jsonify({
            "message": "User created successfully"
        }), 201)
    
    def check_user(self, username):
        user=User.query.filter_by(username=username).first()
        return user
    



@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')


        db_user=User.query.filter_by(username=username).first()
        if db_user is None:
            return make_response(jsonify({"message": "User does not exist"}),403)
        
        if db_user and check_password_hash(db_user.password, password):
            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
