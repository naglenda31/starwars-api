from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_characters = db.Table('user_characters', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True)
)

favorite_planets = db.Table('user_planets', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)

favorite_vehicles = db.Table('user_vehicles', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    characters = db.relationship("Character", secondary=favorite_characters)
    planets = db.relationship("Planet", secondary=favorite_planets)
    vehicles = db.relationship("Vehicle", secondary=favorite_vehicles)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "characters": list(map(lambda x:x.serialize(),self.characters)),
            "planets": list(map(lambda x:x.serialize(), self.planets)),
            "vehicles": list(map(lambda x:x.serialize(), self.vehicles))
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(10))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    homeworld_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    photo_url = db.Column(db.String(250))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld.name
        }

class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    characters = db.relationship("Character", backref='homeworld', lazy=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250))
    rotation_period = db.Column(db.String(250))
    orbital_period = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    population = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.String(250))
    photo_url = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    cost_in_credits = db.Column(db.String(250))
    length = db.Column(db.String(250))
    crew = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    max_atmosphering_speed = db.Column(db.String(250))
    cargo_capacity = db.Column(db.String(250))
    consumables = db.Column(db.String(250))
    photo_url = db.Column(db.String(250))

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
