import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import *

# TOKEN variables
user1_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmODkwOWM4ZWZlMDIwMDY4YzBjMWQ1IiwiYXVkIjoiZGljdGlvbmFyeSIsImlhdCI6MTYxMzIzMzc0NiwiZXhwIjoxNjEzMjQwOTQ2LCJhenAiOiJpSzVCeFJLdUZoWmZkZE5NcUt4RVJ1OVRqZGc5NWdzTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.XvgsgwqiyhQDXLI4TAYfMDNrQ7lUeJ9WOkP2Nb0jRGG2oJggltP4rlFJYShKWmjVcUFhCQp8EcnlbKGAGyrgCBLcWRaKQay839QrnE28XVGBdUNvRWAnIqUh_pCuIpAOTkyDNihMbHZTkMrkkgHN-C_kqR392ePlZoo95ToywugQ5rS2EKH8dB7J9KETAgkyTNxCpQV8OoZDlEuKzQTAtkfb6qFh5lB7HT0jMSKtpTPTqeiOBBgYvyl01GpctNTOF4qe41hQCTLVFbWoElWi0axhFOH79-fShOuHSRff9LKPfZWQR5Qoj2lYAtiB3MIVCbO7sXCSdej5ype1FUvKuQ"
user1_id = "auth0|5ff8909c8efe020068c0c1d5"
user1_wrong_token = ""
admin_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDYzNDc1Nzg1MjAzNDQyOTMzNDMiLCJhdWQiOlsiZGljdGlvbmFyeSIsImh0dHBzOi8vaGVsbG9nYWdhLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTMyMzM3NjksImV4cCI6MTYxMzI0MDk2OSwiYXpwIjoiaUs1QnhSS3VGaFpmZGROTXFLeEVSdTlUamRnOTVnc0wiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnVzZXJzIiwiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OnVzZXJzIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.Osc6GP6C6YVsWRHD9T0Aj-i1l0wkanwe82qF80u5KWf4pio5zvDp6yLcB2ok1s50g1IVApQisCP0Ao1TosfYkR8Pq8Xdxai5sCysdJuHvA0Yj6FbS2IpbGB-v3Uw2k5ctiCRCHI7oQ1vcp31GIsAasIpnh0-XvrIamzAv1lHWJvhr37jBg68Bh1sppvUXwdqiIl6qyXsAc97f6oo2yZIoI973x8VpKMmm8MtD2JsK-2RBBkKT48fAUwjpQ28NlZRso18fkzjxwkqEBAz4lZJXdBkr2MS6P_Ypl-uu9ZhKk69diEoBAr-T6cO3wysCaNW-JnpsFSqUTqrvt5f5ZufdQ"
delete_user_id ="google-oauth2|104536530909866680796"

# unittest.TestLoader.sortTestMethodsUsing = None
class DictionaryTestCase(unittest.TestCase):
  """This class represents the Dictionary test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    # Token for a normal user
    self.user1_id = user1_id
    self.user1_headers = {"Authorization": "Bearer {}".format(user1_token)}
    self.user1_wrong_headers = {"Authorization": "Bearer {}".format(user1_wrong_token)}
    
    # Token for admin
    self.admin_headers={"Authorization": "Bearer {}".format(admin_token)}
    self.admin_wrong_token={"Authorization": "Bearer {}".format(user1_token)}

    # User id to be deleted
    self.usertodelete_id = delete_user_id
    
    # Initiate the APP
    self.app = app
    self.client = self.app.test_client
    self.username = 'postgres'
    self.password = '123456'
    self.database_name = "dict_test"
    self.database_path = "postgres://{}:{}@{}/{}".format(self.username,self.password,'127.0.0.1:5432', self.database_name)
    setup_db(self.app, self.database_path) # the datababase is connected to "dict_test"


    # # binds the app to the current context
    # with self.app.app_context():
      # self.db = SQLAlchemy()
      # self.db.init_app(self.app)
      # create all tables
      # self.db.create_all()

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
    self.assertEqual(response.status_code,200)
  
  def test_get_categories(self):
    '''
    test GET 'categories'
    '''
    # get response
    response = self.client().get('/categories')
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data["success"], True)
    self.assertEqual(data['total_categories'],4)


  def test_get_words_of_a_user(self):
    '''
    test GET '/words', right token
    '''
    # get response
    response = self.client().get('/words', headers=self.user1_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
  
  def test_get_words_of_a_user_no_token(self):
    '''
    test GET '/words', wrong token
    '''
    # get response
    response = self.client().get('/words', headers=self.user1_wrong_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,401)
    self.assertEqual(data['description'], 'Token not found.')
    
  def test_get_a_word_by_id(self):
    '''
    test GET '/words/<int:word_id', right token, the word belongs to the user
    '''
    # get response
    response = self.client().get('/words/6', headers=self.user1_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
  
  def test_get_a_word_by_id_user_has_no_access(self):
    '''
    test GET '/words/<int:word_id', right token, the word does NOT belongs to the user
    '''
    # get response
    response = self.client().get('/words/1', headers=self.user1_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], "Not found")
  
  def test_delete_a_word_by_id(self):
    '''
    test delete '/words/<int:word_id', right token, the word belongs to the user
    '''
    # get response
    response = self.client().delete('/words/7', headers=self.user1_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
  
  def test_delete_a_word_by_id_user_has_no_access(self):
    '''
    test delete '/words/<int:word_id', right token, the word does NOT belong to the user
    '''
    # get response
    response = self.client().delete('/words/1', headers=self.user1_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], "Not found")
  
  def test_patch_a_word_by_id(self):
    '''
    test patch '/words/<int:word_id', right token, the word belongs to the user
    '''
    json_data = {
      'swedishword':'jag',
      'meaninginenglish':'I',
      'meaninginswedish':'random meaning',
      'note':'important'
    }

    # get response
    response = self.client().patch('/words/8', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['updated_word'], 'jag')
  
  def test_patch_a_word_by_id_user_has_no_access(self):
    '''
    test patch '/words/<int:word_id', right token, the word does NOT belong to the user
    '''
    json_data = {
      'swedishword':'jag',
      'meaninginenglish':'I',
      'meaninginswedish':'random meaning',
      'note':'important'
    }
    # get response
    response = self.client().patch('/words/1', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], "Not found")
  
  def test_post_a_word(self):
    '''
    test post '/words', right token
    '''
    json_data = {
      'category_id':3,
      'swedishword':'utblidning',
      'meaninginenglish':'education',
      'meaninginswedish':'random meaning random',
      'note':'important remember'
    }
    # get response
    response = self.client().post('/words', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['word'], 'utblidning')

  def test_post_a_word_not_right_data(self):
    '''
    test post '/words', right token, not right data
    '''
    json_data = {
      'category_id':3,
      'meaninginenglish':'education',
      'meaninginswedish':'random meaning random',
      'note':'important, remember'
    }
    # get response
    response = self.client().post('/words', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,422)
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
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
  
  def test_get_a_question_wrong_token(self):
    '''
    test get '/questions', wrong token
    '''
    # get response
    response = self.client().get('/questions', headers=self.user1_wrong_headers)
    data = json.loads(response.data)
    # make assertation
    self.assertEqual(response.status_code,401)
    self.assertEqual(data['description'], 'Token not found.')
  
  def test_get_answers_for_word_exist(self):
    '''
    test get '/words/9/answers', right token
    '''
    # get response
    response = self.client().get('/words/9/answers', headers=self.user1_headers)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
  
  def test_get_answers_for_word_not_exist(self):
    '''
    test get '/words/9/answers', right token
    '''
    # get response
    response = self.client().get('/words/100/answers', headers=self.user1_headers)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,422)
    self.assertEqual(data['success'], False)
  
  def test_post_a_answer_for_word_exist(self):
    '''
    test post '/words/9/answers', right token
    '''
    json_data = {
      'result':True
    }
    # get response
    response = self.client().post('/words/9/answers', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['message'], 'new answer record was added')
  
  def test_post_a_answer_for_word_user_no_access(self):
    '''
    test post '/words/1/answers', user has no access 
    '''
    json_data = {
      'result':True
    }
    # get response
    response = self.client().post('/words/1/answers', headers=self.user1_headers, json=json_data)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,404)
    self.assertEqual(data['success'], False)


  def test_get_all_users(self):
    '''
    test get '/users', user has admin access
    '''
    # get response
    response = self.client().get('/users', headers=self.admin_headers)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,200)
  
  def test_get_all_users_wrong_token(self):
    '''
    test get '/users' with a normal user token
    '''
    # get response
    response = self.client().get('/users', headers=self.user1_headers)
    data = json.loads(response.data)
    
    # make assertation
    self.assertEqual(response.status_code,401)
    self.assertEqual(data['description'], 'Permission not found.')
  
  def test_delete_a_uesr(self):
    '''
    test delete '/users/<user_id>' with a admin token
    '''
    user1_id = self.usertodelete_id
    # get response
    response = self.client().delete('/users/'+user1_id, headers=self.admin_headers)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code,200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['user'], user1_id)
  
  def test_delete_a_uesr_wrong_token(self):
    '''
    test delete '/users/<user_id>' with a normal user token
    '''
    user1_id = self.usertodelete_id
    # get response
    response = self.client().delete('/users/'+user1_id, headers=self.user1_headers)
    data = json.loads(response.data)

    # make assertation
    self.assertEqual(response.status_code,401)
    self.assertEqual(data['description'], 'Permission not found.')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
