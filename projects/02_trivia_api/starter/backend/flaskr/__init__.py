import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def introspect():
        return jsonify({'message': 'This is an app.'})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
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
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        category_types = [category.type.lower() for category in categories]
        return jsonify({
            "success": True,
            "categories": category_types
        })

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, int)
        # self TODO: The model should be changed to have a relationship to use
        # joins instead
        # self TODO: Allow frontend to send page numbers in request. Now it
        # will get only first page by default.
        ques_entries = Question.query.all()
        total_questions = len(ques_entries)
        if total_questions < (page - 1) * 10:
            abort(400, {"page value out of bounds"})
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
                "currentCategory": "science"
            })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
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

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
