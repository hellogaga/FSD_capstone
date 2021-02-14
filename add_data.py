import models
from models import (setup_db, Categories, Dictionary, AnswerRecords, 
                    username, password)
from flask import Flask
from random import seed, randint
import sys

# Add example data to the dataset.

def add_records_to_database(app,database_path):
    '''
    function to add data to the database
    '''
    # generate randomness
    seed(1)

    # set up database
    setup_db(app,database_path)
    
    # add data to Categories
    categories = ['Verb', 'Substantiv', 'Adjektive', 'Adverb']
    for category in categories:
        new_cate = Categories(category)
        new_cate.insert()
    
    # add data to Dictionary
    user_ids = ['google-oauth2|104536530909866680796', 'auth0|5ff8909c8efe020068c0c1d5', 'google-oauth2|104536530909866680796']
    example_words = ['Stockholm', 'nifiken', 'Svenska', 'lathunde', 'Studera']
    example_cate = [2,3,2,2,1]

    for user_id in user_ids:
        for word, category in zip(example_words, example_cate):
            new_word = Dictionary(user_id,word,category,
                                meaninginenglish='random value' + str(randint(0, 100)))
            new_word.insert()


    # for each user, add a random answer record
    for user_id in user_ids:
        answer = True
        questions_user= Dictionary.query.filter(Dictionary.user_id==user_id).all()
        for question in questions_user:
            newanswer_record = AnswerRecords(question.id, user_id, answer)  
            newanswer_record.insert()
    

if __name__ == '__main__':
    app = Flask(__name__)
    database_name = sys.argv[1]
    database_path = "postgres://{}:{}@{}/{}".format(username,password,'localhost:5432', database_name)
    add_records_to_database(app,database_path)