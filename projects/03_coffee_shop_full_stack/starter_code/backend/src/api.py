import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        public endpoint
'''


@app.route('/drinks')
def get_drinks_short():
    try:
        drinks = [description.short() for description in Drink.query.all()]
        print("number of drinks: ", len(drinks))
        return jsonify({"success": True, "drinks": drinks}), 200
    except Exception as e:
        print(e)
        abort(422)


'''
    GET /drinks-detail
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_dertailed(something):
    try:
        drinks = [description.long() for description in Drink.query.all()]
        print("number of drinks: ", len(drinks))
        return jsonify({"success": True, "drinks": drinks}), 200
    except Exception as e:
        print(e)
        abort(422)


'''
    POST /drinks
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(something):
    data = json.loads(request.data)
    try:
        new_drink = Drink(data['title'], str(json.dumps(data['recipe'])))
        new_drink.insert()
        return jsonify({'success': True, "drink": [json.dumps(new_drink.long())]}), 200
    except Exception as e:
        print(e)
        abort(422)


'''
    PATCH /drinks/<id>
'''


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(something, drink_id):
    data = Drink.query.get(drink_id)
    # print(data)
    if not data:
        abort(404)
    try:
        data_dict = json.loads(request.data)
        if "title" in data_dict:
            # print("found patch for title")
            data.title = json.dumps(data_dict['title'])
        if "recipe" in data_dict:
            # print("found patch for recipe")
            data.recipe = json.dumps(data_dict['recipe'])
        data.update()
        return jsonify({"success": True, "drinks": [data.long()]}), 200
    except Exception as e:
        print(e)
        abort(422)


'''
    DELETE /drinks/<id>
'''


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def remove_drink(something, drink_id):
    data = Drink.query.get(drink_id)
    # print(data)
    if not data:
        abort(404)
    try:
        data.delete()
        return jsonify({"success": True, "delete": drink_id}), 200
    except Exception as e:
        print(e)
        abort(422)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
    Error handler for 404
'''


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


'''
    Error handler for 500
'''


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


'''
    Error handler for AuthError
'''


@app.errorhandler(AuthError)
def autherror(error):
    # print(error.error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
