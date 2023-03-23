"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json

api = Blueprint('api', __name__)

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "User doesn't exist"}), 404
    if email != user.email or password != user.password:
        return jsonify({"msg": "Incorrect email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@api.route("/home", methods=["GET"])
@jwt_required()
def home():
    response_body = {
        "msg": "Hello, you are logged in",
    }
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api.route("/signup", methods=["POST"])
def signup():
    body = json.loads(request.data)
    user = User.query.filter_by(email=body["email"]).first()

    if user:
        return jsonify({"msg": "User already exists"}), 404

    new_user = User(
        email = body["email"], 
        password = body["password"],
        first_name = body["first_name"])

    db.session.add(new_user)
    db.session.commit()
    
    response_body = {"msg": "Hello, you have signed up"}
    return jsonify(response_body), 200


@api.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(id=current_user).first()

    if user_query:
        db.session.delete(user_query)
        db.session.commit()
        return jsonify({"msg": "Your account has been deleted"}), 200
    
    if not user_query:
        return jsonify({"msg": "Not able to delete this account"}), 200


@api.route('/profile', methods=['PUT'])
@jwt_required()
def update_account():
    current_user = get_jwt_identity()
    body = json.loads(request.data)
    user_query = User.query.filter_by(id=current_user).first()

    if user_query is None:
        response_body = {"msg": "User doesn't exists"}
        return jsonify(response_body), 400    

    if "email" in body:
        user_query.email =  body["email"]
    if "password" in body:
        user_query.password =  body["password"]
    if "name" in body:
        user_query.name =  body["name"]
    if "last_name" in body:
        user_query.last_name =  body["last_namewebsite_url"]
    if "website_url" in body:
        user_query.website_url =  body["website_url"]
    if "facebook_profile" in body:
        user_query.facebook_profile =  body["facebook_profile"]
    if "instagram_profile" in body:
        user_query.instagram_profile =  body["instagram_profile"]
    if "tiktok_profile" in body:
        user_query.instagram_profile =  body["tiktok_profile"]
    if "business_name" in body:
        user_query.business_name =  body["business_name"]

    db.session.commit()
    return jsonify({"msg": "You information has been updated"}), 200


@api.route("/users", methods=["GET"])
def get_users():
    users_query = User.query.all()
    results = list(map(lambda user: user.serialize(), users_query))

    return jsonify(results), 200

@api.route('/profile', methods=['GET'])
@jwt_required()
def get_user_details():
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(id=current_user).first()
    result = user_query.serialize()

    return jsonify(result), 200