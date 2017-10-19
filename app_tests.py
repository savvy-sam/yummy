import unittest

from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
	    self.app=app.test_client()
    

    def test_index(self):
        indx=self.app.get('/')
        self.assertEqual(indx.status_code, 200) 



    def test_login(self):
    	indx=self.app.get('/login')
    	self.assertEqual(indx.status_code, 200)



    def  test_signup(self):
    	indx=self.app.get('/signup')
    	self.assertEqual(indx.status_code, 200)

    def test_recipes(self):
    	indx=self.app.get('/recipes')
    	self.assertEqual(indx.status_code, 200)