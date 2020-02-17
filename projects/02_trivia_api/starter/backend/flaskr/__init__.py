import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins.
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def introspect():
        return jsonify({'message': 'This is an app.'})

    '''
  Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, DELETE, OPTIONS')
        return response

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    '''
  Error Handlers
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Aw Snap, page not found :("
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request. Check your paramaters again."
        }), 400

    '''
  Endpoint to handle GET requests for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        category_types = [category.type.lower() for category in categories]
        return jsonify({
            "success": True,
            "categories": category_types
        })

    '''
  GET requests for questions,
  including pagination (every 10 questions).
  This endpoint returns a list of questions,
  number of total questions, current category, categories.

  --TEST-- Possibly TOTO: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  self TODO: Fix the frontend. It's broken.
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, int)
        # self TODO: The model should be changed to have a relationship to use
        # joins instead
        ques_entries = Question.query.all()
        total_questions = len(ques_entries)
        if total_questions < (page - 1) * 10:
            abort(400)
        else:
            start = (page - 1) * 10
            end = min(total_questions, page * 10)
            # Format only needed questions. Save resources.
            formatted_ques = [question.format()
                              for question in ques_entries[start:end]]
            # Assume categories are expected to be page independent.
            cat_entries = Category.query.all()
            categories = {category.id: category.type.lower()
                          for category in cat_entries}
            return jsonify({
                "success": True,
                "questions": formatted_ques,
                "totalQuestions": total_questions,
                "categories": categories,
                "currentCategory": "science"  # Decide what should this be.
            })

    '''
  Endpoint to DELETE question using a question ID.
  '''
    @app.route('/questions/<int:ques_id>', methods=['DELETE'])
    def delete_question(ques_id):
        question = Question.query.get(ques_id)
        if question is None:
            return jsonify({
                "success": False
            }), 400

        question.delete()
        return jsonify({
            "success": True
        })

    '''
  Endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.
  '''

    @app.route('/questions/new', methods=['POST'])
    def add_new_question():
        data = json.loads(request.data)
        if data['question'] is ''\
                or data['answer'] is ''\
                or data['category'] is ''\
                or data['difficulty'] is None:
            return jsonify({
                "success": False
            }), 400

        question = Question(data['question'], data['answer'], data[
                            'category'], data['difficulty'])
        question.insert()
        return jsonify({
            "success": True
        })

    '''
  POST endpoint to get questions based on a search term.
  It returns any questions for which the search term   is a substring of the question.
  '''
    @app.route('/questions', methods=['POST'])
    def search_question():
        search_term = json.loads(request.data)['searchTerm']
        pattern = '%{0}%'.format(search_term)
        ques_entries = Question.query.filter(
            Question.question.ilike(pattern)).order_by(Question.category).all()
        formatted_ques = [question.format() for question in ques_entries]
        return jsonify({
            "success": True,
            "questions": formatted_ques,
            "totalQuestions": len(formatted_ques),
            "currentCategory": "art"
        })

    '''
    GET endpoint to get questions based on category.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_for_category(category_id):
        ques_entries = Question.query.filter(
            Question.category == str(category_id)).all()
        if not ques_entries:
            abort(404)
        else:
            formatted_ques = [question.format() for question in ques_entries]
            return jsonify({
                "success": True,
                "questions": formatted_ques,
                "totalQuestions": len(formatted_ques),
                "currentCategory": "art"
            })

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        params = json.loads(request.data)
        previous_ques = params['previous_questions']

        # WARNING: VERY VERY UGLY HACK.
        # DIDN'T HAVE THE PATIENCE TO FIX FRONTEND SENDING WRONG IDS
        # Will have to fix. All and Science are sent with the same code.
        category = str(int(params['quiz_category']['id']) + 1)
        # This can be cached.
        new_questions = Question.query.filter(Question.category == category)

        if len(previous_ques) != 0:
            new_questions = new_questions.filter(
                ~Question.id.in_(previous_ques))

        if new_questions.count() == 0:
            question = None
        else:
            question = random.choice(new_questions.all())

        return jsonify({
            "success": True,
            "question": question
        })

    return app
