#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

#Hellper Function
def find_scientist_by_id(id):
    return Scientist.query.get(id)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Scientists Missions API!"})

@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    scientists_dicts = [scientist.to_dict( rules = ['-missions']) for scientist in scientists]
    return scientists_dicts, 200


@app.get ('/scientists/<int:id>')
def get_scientist(id):
    scientist = find_scientist_by_id(id)
    if scientist:
        return scientist.to_dict(), 200
    return {"error": "Scientist not found"}, 404


@app.route('/scientists', methods=['POST'])
def add_scientist():
    try:
        body = request.get_json()
        new_scientist = Scientist(**body)
        db.session.add(new_scientist)
        db.session.commit()
        return new_scientist.to_dict(), 201
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400
    
@app.patch ('/scientists/<int:id>')
def update_scientist(id):
    scientist = find_scientist_by_id(id)
    if scientist:
        try:
            body = request.get_json()
            for key, value in body.items():
                setattr(scientist, key, value)
            db.session.add(scientist)
            db.session.commit()
            return scientist.to_dict(), 202
        except Exception as e:
            return jsonify({"errors": ["validation errors"]}), 400
    return {"error": "Scientist not found"}, 404

@app.delete ('/scientists/<int:id>')
def delete_scientist(id):
    scientist = find_scientist_by_id(id)
    if scientist:
        db.session.delete(scientist)
        db.session.commit()
        return {"message": "Scientist deleted successfully"}, 204
    else:
        return {"error": "Scientist not found"}, 404



@app.get ('/planets')
def get_planets():
    planets = Planet.query.all()
    planets_dicts = [planet.to_dict( rules = ['-missions']) for planet in planets]
    return planets_dicts, 200


@app.post('/missions')
def add_mission():
    try:
        body = request.get_json()
        new_mission = Mission(**body)
        db.session.add(new_mission)
        db.session.commit()
        return new_mission.to_dict(), 201
    except Exception as e:
        return jsonify({"errors": ["validation errors"]}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
