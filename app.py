import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def welcome_page():
        return 'Nothing to see here!'


    @app.route('/actors', methods=['GET'])
    #@requires_auth('get:actors')
    def get_all_actors():
        actors = Actor.query.all()

        all_actors = []
        for actor in actors:
            all_actors.append(actor.format())

        print(all_actors)
        return jsonify(all_actors)

    @app.route('/actors', methods=['POST'])
    def add_new_actor():
        if request.data:
            data = request.get_json()
        else:
            abort(424)

        # print(data)
        if not 'name' or not 'age' or not 'gender' in data:
            print('Something missing')
            abort(403)

        name = data['name']
        age = data['age']
        gender = data['gender']

        actor = Actor(name=name,age=age,gender=gender)
        actor.insert()

        return jsonify(actor.format())






    return app


app = create_app()

if __name__ == '__main__':
    app.run()
