import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import *

# Get TOKEN and userid from environments.
user1_token = os.environ["USER1TOKEN"]
user1_id = os.environ["USER1ID"]
user1_wrong_token = ""
admin_token = os.environ["ADMINTOKEN"]
delete_user_id = os.environ["USERTODELETE"]

# Get the username and password for the local database
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
test_database = os.environ["TESTDATABASENAME"]


class DictionaryTestCase(unittest.TestCase):
    """This class represents the Dictionary test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # Token for a normal user
        self.user1_id = user1_id
        self.user1_headers = {"Authorization": "Bearer {}".format(user1_token)}
        self.user1_wrong_headers = {
            "Authorization": "Bearer {}".format(user1_wrong_token)}

        # Token for admin
        self.admin_headers = {"Authorization": "Bearer {}".format(admin_token)}
        self.admin_wrong_token = {
            "Authorization": "Bearer {}".format(user1_token)}

        # User id to be deleted
        self.usertodelete_id = delete_user_id

        # Initiate the APP
        self.app = app
        self.client = self.app.test_client
        self.username = username
        self.password = password
        self.database_name = test_database
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.username, self.password, '127.0.0.1:5432', self.database_name)
        # the datababase is connected to "dict_test"
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_index(self):
        '''
        test get_categories
        '''
        # get data
        response = self.client().get('/')
        # make assertation
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        '''
        test GET 'categories'
        '''
        # get response
        response = self.client().get('/categories')
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['total_categories'], 4)

    def test_get_words_of_a_user(self):
        '''
        test GET '/words', right token
        '''
        # get response
        response = self.client().get('/words', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_words_of_a_user_no_token(self):
        '''
        test GET '/words', wrong token
        '''
        # get response
        response = self.client().get('/words',
                                     headers=self.user1_wrong_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], 'Token not found.')

    def test_get_a_word_by_id(self):
        '''
        test GET '/words/<int:word_id', right token,
        the word belongs to the user
        '''
        # get response
        response = self.client().get('/words/6', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_a_word_by_id_user_has_no_access(self):
        '''
        test GET '/words/<int:word_id', right token,
        the word does NOT belongs to the user
        '''
        # get response
        response = self.client().get('/words/1', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_delete_a_word_by_id(self):
        '''
        test delete '/words/<int:word_id', right token,
        the word belongs to the user
        '''
        # get response
        response = self.client().delete('/words/7', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_a_word_by_id_user_has_no_access(self):
        '''
        test delete '/words/<int:word_id', right token,
        the word does NOT belong to the user
        '''
        # get response
        response = self.client().delete('/words/1', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_patch_a_word_by_id(self):
        '''
        test patch '/words/<int:word_id', right token,
        the word belongs to the user
        '''
        json_data = {
            'swedishword': 'jag',
            'meaninginenglish': 'I',
            'meaninginswedish': 'random meaning',
            'note': 'important'
        }

        # get response
        response = self.client().patch('/words/8',
                                       headers=self.user1_headers,
                                       json=json_data)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['updated_word'], 'jag')

    def test_patch_a_word_by_id_user_has_no_access(self):
        '''
        test patch '/words/<int:word_id', right token,
        the word does NOT belong to the user
        '''
        json_data = {
            'swedishword': 'jag',
            'meaninginenglish': 'I',
            'meaninginswedish': 'random meaning',
            'note': 'important'
        }
        # get response
        response = self.client().patch('/words/1',
                                       headers=self.user1_headers,
                                       json=json_data)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_post_a_word(self):
        '''
        test post '/words', right token
        '''
        json_data = {
            'category_id': 3,
            'swedishword': 'utblidning',
            'meaninginenglish': 'education',
            'meaninginswedish': 'random meaning random',
            'note': 'important remember'
        }
        # get response
        response = self.client().post('/words',
                                      headers=self.user1_headers,
                                      json=json_data)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['word'], 'utblidning')

    def test_post_a_word_not_right_data(self):
        '''
        test post '/words', right token, not right data
        '''
        json_data = {
            'category_id': 3,
            'meaninginenglish': 'education',
            'meaninginswedish': 'random meaning random',
            'note': 'important, remember'
        }
        # get response
        response = self.client().post('/words',
                                      headers=self.user1_headers,
                                      json=json_data)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_a_question(self):
        '''
        test get '/questions', right token
        '''
        # get response
        response = self.client().get('/questions', headers=self.user1_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_a_question_wrong_token(self):
        '''
        test get '/questions', wrong token
        '''
        # get response
        response = self.client().get('/questions',
                                     headers=self.user1_wrong_headers)
        data = json.loads(response.data)
        # make assertation
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], 'Token not found.')

    def test_get_answers_for_word_exist(self):
        '''
        test get '/words/9/answers', right token
        '''
        # get response
        response = self.client().get('/words/9/answers',
                                     headers=self.user1_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_answers_for_word_not_exist(self):
        '''
        test get '/words/9/answers', right token
        '''
        # get response
        response = self.client().get('/words/100/answers',
                                     headers=self.user1_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_post_a_answer_for_word_exist(self):
        '''
        test post '/words/9/answers', right token
        '''
        json_data = {
            'result': True
        }
        # get response
        response = self.client().post('/words/9/answers',
                                      headers=self.user1_headers,
                                      json=json_data)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'new answer record was added')

    def test_post_a_answer_for_word_user_no_access(self):
        '''
        test post '/words/1/answers', user has no access
        '''
        json_data = {
            'result': True
        }
        # get response
        response = self.client().post(
            '/words/1/answers', headers=self.user1_headers, json=json_data)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_all_users(self):
        '''
        test get '/users', user has admin access
        '''
        # get response
        response = self.client().get('/users', headers=self.admin_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 200)

    def test_get_all_users_wrong_token(self):
        '''
        test get '/users' with a normal user token
        '''
        # get response
        response = self.client().get('/users', headers=self.user1_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_a_uesr(self):
        '''
        test delete '/users/<user_id>' with a admin token
        '''
        user1_id = self.usertodelete_id
        # get response
        response = self.client().delete('/users/'+user1_id,
                                        headers=self.admin_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user'], user1_id)

    def test_delete_a_uesr_wrong_token(self):
        '''
        test delete '/users/<user_id>' with a normal user token
        '''
        user1_id = self.usertodelete_id
        # get response
        response = self.client().delete('/users/'+user1_id,
                                        headers=self.user1_headers)
        data = json.loads(response.data)

        # make assertation
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
