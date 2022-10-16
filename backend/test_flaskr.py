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
        self.database_password = "password"
        self.database_username = "postgres"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_username, self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app)
            
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                'question': 'Whats the smallest country in the world',
                'answer': 'Vatican',
                'category': 2,
                'difficulty': 1
            }

            self.new_search = {'searchTerm': 'w'}

            self.new_quiz = {'question_prev': [], 'category_quiz': {'type': 'Geography', 'category_id': 2}}


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_questions_behavior(self):
        res = self.client().get('/questions')
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['total_question']))
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_delete_question_behaivor(self):
        res = self.client().get('/question/1')
        data = json.loads(res, data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delected'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['total_questions']))
        self.assertEqual(question, None)

    def test_404_if_question_doesnot_exist(self):
        res = self.client().get('/question/1000')
        data = json.loads(res, data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

    def test_create_question_behaivor(self):
        res = self.client().post('/question/create', json=self.new_question)    
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['total_questions']))

    def test_search_questions_behaivor(self):
        res = self.client().post('/question/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'], True)
        self.assertTrue(len(data['total_questions']))

    def test_quiz_behavior(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']),
        self.assertEqual(data['question_previous'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()