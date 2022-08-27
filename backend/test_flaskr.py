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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
     
    def verif_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True) 
        
    def verif_post_question(self):
        res = {'question': 'why you cry',
            'answer': 'im afraid',
            'difficulty': 4,'category': 1}
        res = self.client().post('/questions', json=res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
   
    def verif_do_search(self):
        search = {'searchTerm': 'hou', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        
    def verif__questions_in_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'horror')
    
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
        self.assertEqual(data['success'], True)
        
        
    
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
