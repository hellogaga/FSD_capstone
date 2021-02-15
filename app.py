import json
import dateutil.parser
import babel
from flask import (Flask, render_template,
                   request, Response, flash,
                   redirect, url_for, abort, jsonify)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from models import *
from datetime import datetime
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
import random
import os
import sys

# --------------------------------------------------------------- #
'''Variables'''
# --------------------------------------------------------------- #
QUESTIONS_PER_PAGE = 10


# --------------------------------------------------------------- #
'''Initial APP'''
# --------------------------------------------------------------- #


# Create app
app = Flask(__name__)
setup_db(app)  # by default, the app will be connected to "dict"

# CORS setup
CORS(app, resources={r"/*": {"origins": '*'}})


@app.after_request
def after_request(response):
    # response.
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


def paginate_words(request, selection):
    '''
    function to paginate the responses
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    words = [word.format() for word in selection]
    current_questions = words[start:end]

    return current_questions


# --------------------------------------------------------------- #
'''Endpoints for normal users'''
# --------------------------------------------------------------- #


# Index page, no permission needed
@app.route('/')
def index():
    '''
    Index page, only show a message
    '''
    return 'Welcome to a Dictionary API'


# get word categories, no permisson needed
@app.route('/categories', methods=['GET'])
def get_categories():
    '''
    Show categories of words. Universial for all users.
    This needs no permission
    '''
    # get categoreis
    categories = Categories.query.order_by(Categories.id).all()
    # make a dict
    categories_output = [category.format() for category in categories]
    categorie_nr = len(categories)

    print(categories_output)

    # check if abort
    if categorie_nr == 0:
        abort(404)
    # return results
    return jsonify({
        'success': True,
        'categories': categories_output,
        'total_categories': categorie_nr
    }), 200


# /words, permission required
@app.route('/words', methods=['GET'])
@requires_auth('get:words')
def get_swedish_words(jwt_payload):
    '''
    endpoint for get all words for a specific user
    words are displayed in pages.
    permission checked
    '''
    # get user from payload
    user_id = jwt_payload['sub']
    # get questions
    words = Dictionary.query.filter(Dictionary.user_id == user_id).all()

    # abort if no words
    if len(words) == 0:
        abort(404)

    # paginate questions
    question_nr = len(words)
    selected_words = paginate_words(request, words)

    if len(selected_words) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': selected_words,
        'total_questions': question_nr,
    })


# /words/<int:question_id>, get a specific word by word id
@app.route('/words/<int:word_id>', methods=['GET'])
@requires_auth('get:words')
def get_a_word(jwt_payload, word_id):
    '''
    endpoint to 'get' a specific word
    permission will be checked
    ONLY show the word when it belongs to the users
    '''
    # get user id
    user_id = jwt_payload['sub']
    word = Dictionary.query.\
        filter(Dictionary.user_id == user_id).\
        filter(Dictionary.id == word_id).one_or_none()

    if word is None:
        abort(404)

    return jsonify({
        'success': True,
        'word': word.format()
    })


# /words/<int:question_id>, delete a specific word by word id
@app.route('/words/<int:word_id>', methods=['DELETE'])
@requires_auth('delete:words')
def delete_function(jwt_payload, word_id):
    '''
    endpoint to 'delete' a specific word
    This is only possible when the word belongs to the user.
    '''
    user_id = jwt_payload['sub']

    word = Dictionary.query.\
        filter(Dictionary.user_id == user_id).\
        filter(Dictionary.id == word_id).one_or_none()

    if word is None:
        abort(404)

    try:
        # need also delete the answerrecords
        related_answer_records = AnswerRecords.query.\
            filter(AnswerRecords.dict_id == word.id).all()
        for record in related_answer_records:
            record.delete()
        word.delete()
        leftwords = Dictionary.query.filter(
            Dictionary.user_id == user_id).all()
        if leftwords is None:
            left_nr = 0
        else:
            left_nr = len(leftwords)

        return jsonify({
            'success': True,
            'deleted': word_id,
            'total_left_words': left_nr
        })
    except SQLAlchemyError as e:
        # abort if error happens
        print(sys.exc_info())
        abort(422)


# /words/int_id
@app.route('/words/<int:word_id>', methods=['PATCH'])
@requires_auth('patch:words')
def patch_a_word(jwt_payload, word_id):
    '''
    Endpoint for revise a word.
    Permission is checked.
    '''
    user_id = jwt_payload['sub']
    # check if drink exists
    word = Dictionary.query.\
        filter(Dictionary.user_id == user_id).\
        filter(Dictionary.id == word_id).one_or_none()
    if word is None:
        abort(404)

    try:
        # check the input data
        data = request.get_json()
        if 'swedishword' in data:
            word.swedishword = data['swedishword']
        if 'meaninginenglish' in data:
            word.meaninginenglish = data['meaninginenglish']
        if 'meaninginswedish' in data:
            word.meaninginswedish = data['meaninginswedish']
        if 'note' in data:
            word.note = data['note']

        # update the word
        word.update()
    except SQLAlchemyError as e:
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'updated_word': word.swedishword
    }), 200


# /words, add a new word to dictionary. Permission required
@app.route('/words', methods=['POST'])
@requires_auth('post:words')
def post_a_new_word(jwt_payload):
    '''
    Endpoint for create a new word.
    Permission is checked.
    '''
    # check
    user_id = jwt_payload['sub']

    # check input data
    data = request.get_json()
    if 'swedishword' not in data:
        abort(422)

    # Insert the new word
    try:
        new_word = Dictionary(user_id, data['swedishword'],
                              data['category_id'],
                              meaninginenglish=data['meaninginenglish'],
                              meaninginswedish=data['meaninginswedish'],
                              note=data['note'])
        new_word.insert()
        print('inserted')
    except SQLAlchemyError as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

    # return message
    return jsonify({
        'success': True,
        'word': new_word.swedishword
    }), 200


# /questions, get random questions
@app.route('/questions', methods=['GET'])
@requires_auth('get:questions')
def get_a_question(jwt_payload):
    '''
    End point to get a random question from database.
    '''
    user_id = jwt_payload['sub']
    try:
        random_words = Dictionary.query.\
            filter(Dictionary.user_id == user_id).\
            order_by(func.random()).limit(3)

    except SQLAlchemyError as e:
        db.session.rollback()
        abort(422)

    word_id = random_words[0].id
    question = random_words[0].swedishword
    choices = [xx.meaninginenglish for xx in random_words]
    random.shuffle(choices)
    answer = random_words[0].meaninginenglish

    return jsonify({
        'success': True,
        'word_id': word_id,
        'question': question,
        'choices': choices,
        'answer': answer
    }), 200


# /words/<int:word_id>/answers
# Get the history of answers
@app.route('/words/<int:word_id>/answers', methods=['GET'])
@requires_auth('get:answers')
def get_answer_history(jwt_payload, word_id):
    '''
    Get the answer history for a specific question
    permission will be checked.
    '''
    # get the user
    user_id = jwt_payload['sub']
    # get the word
    A_word = Dictionary.query.\
        filter(Dictionary.user_id == user_id).\
        filter(Dictionary.id == word_id).one_or_none()
    if A_word is None:
        abort(422)
    # get the answer history
    answers_history = A_word.answer_record.all()

    if len(answers_history) == 0:
        records = []
    else:
        records = [record.format() for record in answers_history]

    return jsonify({
        'success': True,
        'Answer history': records
    }), 200


# /words/<int:id>/answers
# post a new answer
@app.route('/words/<int:word_id>/answers', methods=['POST'])
@requires_auth('post:answers')
def post_A_answer(jwt_payload, word_id):
    '''
    post a new answer to a new question
    '''
    # get the user
    user_id = jwt_payload['sub']

    # check the word belongs to the user
    word = Dictionary.query.get(word_id)
    if word is None:
        abort(404)

    if word.user_id != user_id:
        abort(404)

    # check input data
    data = request.get_json()
    if 'result' not in data:
        abort(422)

    # Insert the new word
    try:
        new_record = AnswerRecords(dict_id=word_id,
                                   user_id=user_id,
                                   result=data['result'])
        new_record.insert()

    except SQLAlchemyError as e:
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

    # return message
    return jsonify({
        'success': True,
        'message': 'new answer record was added',
        'word_id': word_id
    }), 200


# --------------------------------------------------------------- #
'''Endpoints for Admin user'''
# --------------------------------------------------------------- #


# /users
# endpoint to get all users. Permission needed
@app.route('/users', methods=['GET'])
@requires_auth('get:users')
def get_users(jwt_payload):
    # get users in the database
    try:
        allusers = db.session.query(Dictionary.user_id).distinct().all()
        users = [user[0] for user in allusers]
        # get the records numbers.
        user_data_detail = []
        for user in users:
            # get the word numbers
            word_records = Dictionary.query.\
                filter(Dictionary.user_id == user).all()
            if word_records is not None:
                word_nr = len(word_records)
            else:
                word_nr = 0

            # get the records numbers
            answer_records = AnswerRecords.query.\
                filter(AnswerRecords.user_id == user).all()
            if answer_records is not None:
                answer_nr = len(answer_records)
            else:
                answer_nr = 0

            user_data_detail.append({
                'user': user,
                'number of words': word_nr,
                'number of answers': answer_nr
            })

    except SQLAlchemyError as e:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'users': users,
        'user data': user_data_detail
    }), 200


# /users/<user_id>
# delete data of a specific user. Permission needed
@app.route('/users/<user_id>', methods=['DELETE'])
@requires_auth('delete:users')
def delete_a_user(jwt_payload, user_id):

    # Try delete all info of a user
    try:
        answer_records = AnswerRecords.query.\
            filter(AnswerRecords.user_id == user_id).all()

        if answer_records is not None:
            answer_nr = len(answer_records)
            for record in answer_records:
                record.delete()

        words = Dictionary.query.\
            filter(Dictionary.user_id == user_id).all()

        if words is not None:
            word_nr = len(words)
            for word in words:
                word.delete()

    # if error happens
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(422)

    # if success
    return jsonify({
        'success': True,
        'user': user_id,
        'deleted words': word_nr,
        'deleted answers': answer_nr,
    }), 200


# --------------------------------------------------------------- #
'''Error Handling'''
# --------------------------------------------------------------- #


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request error'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'An internal error has occured'
    }), 500


@app.errorhandler(AuthError)
def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response


# --------------------------------------------------------------- #
'''Run the APP'''
# --------------------------------------------------------------- #

# Default port:
if __name__ == '__main__':
    app.run(debug=True)
