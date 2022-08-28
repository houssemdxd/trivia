import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD,DB_HOST


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
      
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_by_categories(self):
     res = self.client().get('/categories')
     data = json.loads(res.data)
     self.assertEqual(res.status_code, 200)
     self.assertEqual(data["success"], True)
     self.assertTrue(data["categories"])
     
    def test_get_categories_not_allowed(self):
        res = self.client().patch('/categories')
        self.assertEqual(res.status_code, 405)   
   
   
    """def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True) """
        
        
    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        
     
    def test_post_question(self):
        res = {'question': 'why you cry',
            'answer': 'im afraid',
            'difficulty': 4,'category': 1}
        res = self.client().post('/questions', json=res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    def test_post_questionerror(self):
        res = {'question': 'why you cry',
            'answer': 'im afraid','abc':'mmm'}
        a=0
        res = self.client().post('/questions', json=a)
        
        self.assertEqual(res.status_code, 422)
            
        
    def test_search_not_found(self):
        search = {
            'searchTerm': 'azrt55kkhgjgjhgfukg555',
        }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
      
        self.assertEqual(res.status_code,404)      
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
        
    def test_get_categories_not_allowed(self):
        res = self.client().patch('/questions')
        self.assertEqual(res.status_code, 405)         
        
         
    def test__questions_in_category(self):
        #you can change category_id value it to suit with your need
        category_id=2
        res = self.client().get('/categories/'+str(category_id)+'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       
        self.assertEqual(data['currentCategory'], Category.query.filter(Category.id==category_id).first().type)
        
    def test_questions_in_category_not_found(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
       
    def test_do_search(self):
        search = {'searchTerm': 'what', }
        res = self.client().post('/questions', json=search)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
    
    def test_quiz(self):
        quiz = {
            'previous_questions': [1],
            'quiz_category': {
                'type': 'a',
                'id': '1'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
       
        
    
    def test_quiz_not_found_(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': 'abcd',
                'id': '8787878'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
