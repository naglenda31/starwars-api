"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)


    user = User.query.filter_by(username=username).first()
    if user is None or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/user', methods=['PUT'])
def handle_users():
    users = User.query.all()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": list(map(lambda x:x.serialize(),users))
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['PUT'])
def update_user_favorites():
    user_id = request.json.get("user_id", None)
    #add if variable is None, show error
    resource_id = request.json.get("id", None)
    resource_type = request.json.get("type", None)

    user = User.query.get(user_id)

    if resource_type == "character":
        resource = Character.query.get(resource_id)
        user.characters.append(resource)
    if resource_type == "planet":
        resource = Planet.query.get(resource_id)
        user.planets.append(resource)

    if resource_type == "vehicle":
        resource = Vehicle.query.get(resource_id)
        user.vehicles.append(resource)

    response_body = {
        "msg": "Resource added successfully",
        "user": user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def handle_characters():
    characters = Character.query.all()
    response_body = {
        "msg": "These are characters",
        "characters": list(map(lambda x:x.serialize(), characters))
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    response_body = {
        "msg": "These are planets", 
        "planets": list(map(lambda x:x.serialize(), planets))
    }

    return jsonify(response_body), 200

@app.route('/vehicle', methods=['GET'])
def handle_vehicles():
    vehicles = Vehicle.query.all()
    response_body = {
        "msg": "These are vehicles", 
        "vehicles": list(map(lambda x:x.serialize(), vehicles))
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
