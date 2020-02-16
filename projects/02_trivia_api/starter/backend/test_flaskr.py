import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_invalid_page_gives_bad_request(self):
        res = self.client().get('/questions?page=100')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)['success'], False)
        pass

    def assert_valid_request(self, res, data, total_questions=None):
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        if total_questions is not None:
            self.assertEqual(data['totalQuestions'], total_questions)
        pass

    def test_get_questions_returns_count_of_all(self):
        res = self.client().get('/questions')
        self.assert_valid_request(res, json.loads(res.data), 19)
        pass

    def test_get_questions_is_poginated(self):
        res_1 = self.client().get('/questions')
        data_full_page = json.loads(res_1.data)
        self.assert_valid_request(res_1, data_full_page, 19)
        self.assertEqual(len(data_full_page['questions']), 10)

        res_2 = self.client().get('/questions?page=2')
        data_incomplete_page = json.loads(res_2.data)
        self.assert_valid_request(res_2, data_incomplete_page, 19)
        self.assertEqual(len(data_incomplete_page['questions']), 9)
        pass

    def test_categories_returns_all(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assert_valid_request(res, data)
        self.assertEqual(len(data['categories']), 6)
        pass

    def test_invalid_category_id_bad_request(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)['success'], False)
        pass

    def assert_questions_for_category_count(self, category_id, count):
        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)
        self.assert_valid_request(res, data, count)
        self.assertEqual(len(data['questions']), count)
        pass

    def test_question_count_for_all_categories(self):
        self.assert_questions_for_category_count(1, 3)
        self.assert_questions_for_category_count(2, 4)
        self.assert_questions_for_category_count(3, 3)
        self.assert_questions_for_category_count(4, 4)
        self.assert_questions_for_category_count(5, 3)
        self.assert_questions_for_category_count(6, 2)
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
