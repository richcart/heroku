from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def welcome_page():
        return 'Nothing to see here, yet!'

    @app.route('/login-results', methods=['GET'])
    def redirect_from_login():
        token = request.args['access_token']
        return (token)

    # ROUTES FOR ACTORS

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_all_actors(payload):
        actors = Actor.query.all()

        all_actors = []
        for actor in actors:
            all_actors.append(actor.format())

        return jsonify({
            'success': True,
            'actors': all_actors
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_new_actor(payload):
        if request.data:
            data = request.get_json()
        else:
            abort(400)

        if not 'name' in data:
            print('Please provide a name')
            abort(403)

        if not 'age' in data:
            print('Please provide a age')
            abort(403)

        if not 'gender' in data:
            print('Please provide a gender')
            abort(403)

        name = data['name']
        age = data['age']
        gender = data['gender']

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.get_or_404(id)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted_id': id
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        if request.data:
            data = request.get_json()
        else:
            abort(400)

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.get_or_404(id)

        if name:
            actor.name = name

        if age:
            actor.age = age

        if gender:
            actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # ROUTES FOR MOVIES

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_all_movies(payload):
        movies = Movie.query.all()

        all_movies = []
        for movie in movies:
            all_movies.append(movie.format())

        print(all_movies)
        return jsonify({
            'movies': all_movies,
            'success': True
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_new_movie(payload):
        if request.data:
            data = request.get_json()
        else:
            abort(400)

        if not 'title' in data:
            print('Please provide a title')
            abort(403)

        if not 'release_date' in data:
            print('Please provide a release date')
            abort(403)

        title = data['title']
        release_date = data['release_date']

        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.get_or_404(id)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted_id': id
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        if request.data:
            data = request.get_json()
        else:
            abort(400)

        movie = Movie.query.get_or_404(id)

        title = data.get('title', None)
        release_date = data.get('release_date', None)

        if title:
            movie.title = title

        if release_date:
            movie.release_date = release_date

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # SETTING UP ERROR HANDLING

    @app.errorhandler(400)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def not_authorised(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorised"
        }), 401

    @app.errorhandler(403)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "not authorsied"
        }), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
