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

        self.new_actor_without_name = {
            'age': '21',
            'gender': 'Male'
        }

        self.patch_actor = {
            'name': 'Bob Jones'
        }

        self.patch_movie = {
            'title': 'A Song for Summer'
        }

        self.new_movie = {
            'title': 'Never Say Boo',
            'release_date': '2020-05-12'
        }

        self.new_movie_without_title = {
            'release_date': '2020-05-22'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TESTS FOR FUNCTIONALITY OF ENDPOINTS

    # ACTOR ENDPOINTS

    def test_get_all_actors_without_auth(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_all_actors_with_auth(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.jwt_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_add_new_actor_as_assistant(self):
        print(self.jwt_assistant)
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_assistant})
        self.assertEqual(403, res.status_code)

    def test_add_new_actor_as_director(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_director})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], self.new_actor['name'])
        self.assertEqual(data['actor']['age'], self.new_actor['age'])
        self.assertEqual(data['actor']['gender'], self.new_actor['gender'])

    def test_add_new_actor_as_producer_incomplete_data(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor_without_name),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(403, res.status_code)

    def test_add_and_delete_actor_as_director(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_actor),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_director})

        data = json.loads(res.data)
        id = data['actor']['id']
        res2 = self.client().delete('/actors/' + str(id),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_director})

        data2 = json.loads(res2.data)
        self.assertEqual(200, res2.status_code)
        self.assertTrue(data2['success'])

    def test_delete_actor_as_assistant(self):
        res = self.client().delete('/actors/1',
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_assistant})
        self.assertEqual(403, res.status_code)

    def test_delete_unknown_actor_as_producer(self):
        res = self.client().delete('/actors/10000',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(404, res.status_code)

    def test_update_actor_as_producer(self):
        res = self.client().patch('/actors/1',
                                   data=json.dumps(self.patch_actor),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(200, res.status_code)

    def test_update_actor_as_producer_without_data(self):
        res = self.client().patch('/actors/1',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(400, res.status_code)

    # MOVIE ENDPOINTS

    def test_get_all_movies_without_auth(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_all_movies_with_auth(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + self.jwt_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_add_new_movie_as_assistant(self):
        print(self.jwt_assistant)
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_assistant})
        self.assertEqual(403, res.status_code)

    def test_add_new_movie_as_producer(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_add_new_movie_as_producer_incomplete_data(self):
        res = self.client().post('/actors',
                                 data=json.dumps(self.new_movie_without_title),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(403, res.status_code)

    def test_add_and_delete_movie_as_producer(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})

        data = json.loads(res.data)
        id = data['movie']['id']
        res2 = self.client().delete('/movies/' + str(id),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + self.jwt_producer})

        data2 = json.loads(res2.data)
        self.assertEqual(200, res2.status_code)
        self.assertTrue(data2['success'])

    def test_delete_movie_as_assistant(self):
        res = self.client().delete('/movies/1',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + self.jwt_assistant})
        self.assertEqual(403, res.status_code)

    def test_delete_unknown_movie_as_producer(self):
        res = self.client().delete('/movies/10000',
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(404, res.status_code)

    def test_update_movie_as_producer(self):
        res = self.client().patch('/movies/1',
                                  data=json.dumps(self.patch_movie),
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(200, res.status_code)

    def test_update_movie_as_producer_without_data(self):
        res = self.client().patch('/movies/1',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(400, res.status_code)

    # TESTS FOR ROLE ACCESS

    def test_add_new_movie_as_role_assistant(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_assistant})
        self.assertEqual(403, res.status_code)

    def test_add_new_movie_as_role_director(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_director})
        self.assertEqual(403, res.status_code)

    def test_add_new_movie_as_role_producer(self):
        res = self.client().post('/movies',
                                 data=json.dumps(self.new_movie),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + self.jwt_producer})
        self.assertEqual(200, res.status_code)

    def test_get_all_actors_as_role_assistant(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.jwt_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_all_actors_as_role_director(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.jwt_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_all_actors_as_role_producer(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + self.jwt_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
