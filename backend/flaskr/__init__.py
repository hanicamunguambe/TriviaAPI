
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

import collections
collections.Iterable = collections.abc.Iterable
QUESTIONS_PER_PAGE = 10

def paginate_question(request, selection):
    #implementing pagition
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    data_questions = [question.format() for question in selection]
    current_questions = data_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
   
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #basic initialization cors
    CORS(app, resources={r"/api/*": {"origins": "*"}})
     

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Autorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def categories():
        categories = Category.query.all()
        
        data_categories = {category.id: category.type for category in categories}

        return jsonify ({
             'success': True,
             'categories': data_categories
        }) 
            
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def questions():
        #get request for question n category
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, selection)
        categories = Category.query.all()
        if len(current_questions) == 0:
            abort(404)
       
        data_categories = {category.id: category.type for category in categories}

        return jsonify ({
            'success': True,
            'questions': current_questions,
            'total_question': len(selection),
            'current_category': None,
            'categories': data_categories
        }) 

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods = ['DELETE'])
    def delete_question(question_id):
        
        try:
          question = Question.query.filter(Question.id == question_id).one_or_none()

          if question is None:
            abort(404)
            
          question.delete()
          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_question(request, selection)

          return jsonify({
                'success': True,
                'delected': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all()) 
          })
        except:
          abort(422)
        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/question/create', methods = ['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/question/search', methods=['POST'])
    def search_questions(): 
        body = request.get_json()
        search_term = body.get('search', None)
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_question(request, selection)
        
        if selection == None: 
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection)
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions>')
    def questions_category(category_id):

        try:
            selection =  Question.query.filter(Question.category == category_id).one_or_none()
            current_questions = paginate_question(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
            })
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():

        try:
            body = request.get_json()
            category_quiz = body.get('category_quiz')
            question_prev = body.get('question_prev')
            category_id = category_quiz['id']

            if category_id == 0:
                questions_data = Question.query.filter(Question.id.notin_(question_prev)).all()
            else:
                questions_data = Question.query.filter(Question.id.notin_(question_prev), Question.category == category_id).all()
                questions = None
                if(questions_data):
                    questions = random.choice(questions_data)

                return jsonify({
                    'success': True,
                    'question': questions.format(),
                    'question_previous': question_prev
                })
        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resouce not found'
        }), 404

    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'request cannot be processed'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        })
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        })

    return app

