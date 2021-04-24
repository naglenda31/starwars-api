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
from models import db, User, Person, Planet, Vehicle

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

#Endpoint to retrieve all users
@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    response_body = {
        "msg": "These are all users",
        "users": list(map(lambda x:x.serialize(),users))
    }

    return jsonify(response_body), 200

#Endpoint to retrieve one user by id
@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    response_body = {
        "user": user.serialize()
    }
   
    return jsonify(response_body), 200

#Endpoint to add to favorites
@app.route('/user', methods=['PUT'])
def update_user_favorites():
    user_id = request.json.get("user_id", None)
    resource_id = request.json.get("id", None)
    resource_type = request.json.get("type", None)

    if user_id is None:
        return jsonify({"msg": "No user id specified"}), 400
    if resource_id is None:
        return jsonify({"msg": "No resource id specified"}), 400
    if resource_type is None:
        return jsonify({"msg": "No resource type specified"}), 400

    user = User.query.get(user_id)

    if User is None:
        return jsonify({"msg": "No user was found"}), 400

    if resource_type == "person":
        resource = Person.query.get(resource_id)
        user.people.append(resource)
    if resource_type == "planet":
        resource = Planet.query.get(resource_id)
        user.planets.append(resource)

    if resource_type == "vehicle":
        resource = Vehicle.query.get(resource_id)
        user.vehicles.append(resource)

    db.session.commit()

    response_body = {
        "msg": "Resource added successfully",
        "user": user.serialize()
    }

    return jsonify(response_body), 200

#Endpoint to retrieve all characters
@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    response_body = {
        "msg": "These are characters",
        "characters": list(map(lambda x:x.serialize(), people))
    }

    return jsonify(response_body), 200

#Endpoint to retrieve one character by id
@app.route('/people/<id>', methods=['GET'])
def get_person_by_id(id):
    person = Person.query.get(id)
    response_body = {
        "msg": "This is a character",
        "character": person.serialize()
    }
   
    return jsonify(response_body), 200

#Endpoint to retrieve planets
@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    response_body = {
        "msg": "These are planets", 
        "planets": list(map(lambda x:x.serialize(), planets))
    }

    return jsonify(response_body), 200

#Endpoint to retrieve one planet by id
@app.route('/planet/<id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planet.query.get(id)
    response_body = {
        "msg": "This is a planet", 
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

#Endpoint to retrieve all vehicles
@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    response_body = {
        "msg": "These are vehicles", 
        "vehicles": list(map(lambda x:x.serialize(), vehicles))
    }

    return jsonify(response_body), 200

#Endpoint to retrieve one vehicle by id
@app.route('/vehicle/<id>', methods=['GET'])
def get_vehicle_by_id(id):
    vehicle = Vehicle.query.get(id)
    response_body = {
        "msg": "This is a vehicle", 
        "vehicle": vehicle.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
