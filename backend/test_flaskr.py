import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_password = DB_PASSWORD
        self.database_username = DB_USER
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

            self.new_search = {'searchTerm': 'who'}

            self.new_quiz = {'question_prev': [], 'category_quiz': {'type': 'Geography', 'category_id': 2}}


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #list all questions case true
    def test_questions_behavior(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
       
    #case error on listin questions
    def test_questions_error(self):
        res = self.client().get('/questions/all')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
   
    #case delete questions by id case true
    def test_delete_question_behaivor(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).first()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)
   
        
    #error delete questions by id case false
    def test_delete_question_error(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
    
    #error if question doesn't exist
    def test_422_if_question_doesnot_exist(self):
     
        res = self.client().get('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #create question case true
    def test_create_question_behaivor(self):
        res = self.client().post('/question/create', json=self.new_question)    
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
       
    #error while creating question case false
    def test_create_question_error(self):
        res = self.client().post('/question/create', json=self.new_question)    
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'], 'error')
    
    #search questions case true
    def test_search_questions_behaivor(self):
        res = self.client().post('/question/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['questions'], False)

    #error search questions case false
    def test_search_questions_error(self):
        res = self.client().post('/question/search', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #list all category case true
    def test_categories_behavior(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    #error list all category case false
    def test_categories_error(self):
        res = self.client().get('/categories/all')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        

    def test_quiz_error(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
  


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()