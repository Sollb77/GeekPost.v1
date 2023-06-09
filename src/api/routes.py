from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

password = os.environ.get("PASSSMTP")
print(password)
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
    return jsonify(access_token=access_token), 200

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
        return jsonify({"msg": "User already exists"}), 403

    new_user = User(
        email = body["email"], 
        password = body["password"],
        first_name = body["first_name"])

    db.session.add(new_user)
    db.session.commit()

    userCreated = User.query.filter_by(email=body["email"]).first()

    access_token = create_access_token(identity=userCreated.id)
    return jsonify(access_token=access_token), 200

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
        response_body = {"msg": "User doesn't exist."}
        return jsonify(response_body), 400    

    if "email" in body:
        user_query.email =  body["email"]
    # if "password" in body:
    #     user_query.password =  body["password"]
    if "name" in body:
        user_query.name =  body["name"]
    if "last_name" in body:
        user_query.last_name =  body["last_namewebsite_url"]
    if "contact_data" in body:
        user_query.contact_data =  body["contact_data"]
    if "facebook_profile" in body:
        user_query.facebook_profile =  body["facebook_profile"]
    if "instagram_profile" in body:
        user_query.instagram_profile =  body["instagram_profile"]
    if "tiktok_profile" in body:
        user_query.instagram_profile =  body["tiktok_profile"]
    if "identity" in body:
        user_query.identity =  body["identity"]
    if "logo" in body:
        user_query.logo =  body["logo"]
    if "main_color" in body:
        user_query.main_color =  body["main_color"]
    if "secondary_color" in body:
        user_query.secondary_color =  body["secondary_color"]
    if "aux_color" in body:
        user_query.aux_color =  body["aux_color"]
    db.session.commit()
    return jsonify({"msg": "You information has been updated"}), 200


@api.route("/users", methods=["GET"])
def get_users():
    users_query = User.query.all()
    results = list(map(lambda user: user.serialize(), users_query))

    return jsonify(results), 200

@api.route('/profile', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user_query = User.query.filter_by(id=current_user).first()
    result = user_query.serialize()

    return jsonify(result), 200

# ROUTES FOR POST TABLE

@api.route("/infopost", methods=["POST"])
@jwt_required()
def save_post_info():
    body = request.get_json()

    current_user = get_jwt_identity()

    new_post = Post(
        user_id = current_user,
        identity = body["identity"],
        main_text = body["main_text"],
        secondary_text = body["secondary_text"],
        price = body["price"],
        logo = body["logo"],
        formality = body["formality"],
        main_color = body["main_color"],
        secondary_color = body["secondary_color"],
        aux_color = body["aux_color"],
        ratio = body["ratio"],
        contact_data = body["contact_data"],
        cta = body["cta"]
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "post": new_post.serialize(), "current_user": current_user}), 201

@api.route("/infopost/", methods=["GET"])
@jwt_required()
def get_post_info():
    current_user = get_jwt_identity()
    post = Post.query.filter_by(user_id=current_user).order_by(Post.id.desc()).first()

    if not post:
        raise Forbidden("No tiene permiso para acceder a este post.")

    return jsonify({"post": post.serialize()}), 200

@api.route("/post/<int:id>/image-url", methods=["POST"])
def add_image_url_to_post(id):
    post = Post.query.get(id)

    if not post:
        return jsonify({"Error": "Post not found."}), 404

    data = request.get_json()

    if not data.get("image_url"):
        return jsonify({"Error": "Not URL present in request."}), 400

    post.image_url = data["image_url"]
    db.session.commit()

    return jsonify({"msg": "URL added to post's registry successfully."}), 200

@api.route('/contact', methods=['POST'])
def handle_contact_form():
    # Verificar que se ha recibido toda la información necesaria
    required_fields = ['name', 'email', 'subject', 'message']
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        error_message = f"Los campos requeridos {', '.join(missing_fields)} no se han enviado"
        return error_message, 400

    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Configurar el mensaje de correo electrónico
    message_body = f"Nombre: {name}\nCorreo electrónico: {email}\nAsunto: {subject}\nMensaje: {message}"
    msg = MIMEMultipart()
    msg['From'] = 'ibai600@gmail.com'
    msg['To'] = 'info@ibaifernandez.com'
    msg['Cc'] = 'info@aglaya.biz'
    msg['Subject'] = "Nuevo mensaje de contacto en GeekPost"
    msg.attach(MIMEText(message_body, 'plain'))

    # Enviar el correo electrónico
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("ibai600@gmail.com", password)
        text = msg.as_string()
        server.sendmail('ibai600@gmail.com', ['info@ibaifernandez.com', 'info@aglaya.biz'], text)
        server.quit()
    except smtplib.SMTPException as e:
        # Manejar errores de conexión o envío de correo electrónico
        return f'Error al enviar el mensaje: {str(e)}', 500

    return 'Mensaje recibido', 200