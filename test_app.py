import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class HerokuTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.jwt_assistant = os.environ['JWT_ASSISTANT']
        self.jwt_director = os.environ['JWT_DIRECTOR']
        self.jwt_producer = os.environ['JWT_PRODUCER']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Bart Barrowman',
            'age': '21',
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Never Say Boo',
            'release_date': '2020-05-12'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors_without_auth(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_all_actors_with_auth(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.jwt_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_add_new_actor_as_assistant(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_assistant})
        #data = json.loads(res.data)
        self.assertEqual(403, res.status_code)

    def test_add_new_actor_as_director(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_director})
        # data = json.loads(res.data)
        self.assertEqual(200, res.status_code)

    def test_add_new_movie_as_producer(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})
        # data = json.loads(res.data)
        self.assertEqual(200, res.status_code)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
