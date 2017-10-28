"""This model defines various methods of testing this flask app"""
import unittest
from app import app
from app.model import User, Recipe


class TestApp(unittest.TestCase):
    """This defines a class TesrApp that inherits from unittest.TesrCase"""

    def setUp(self):
        """This method defines the events to happen before any test runs"""
#creates a test client app
        self.app = app.test_client()
#creates objects of User and Recipe classes
        self.user = User("sam", "sam@gmail.com", 123456, 123456)
        self.recipe = Recipe("recipe example", "This an example of a Recipe") 

    def test_index(self):
        """"This method tests whether the route '/' succesfully renders a page"""
        indx = self.app.get('/')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_register(self):
        """"This method tests whether the route '/register' succesfully renders a page"""
        indx = self.app.get('/register')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_user_update(self):
        """"This method tests whether the route '/user/update' succesfully renders a page"""
        indx = self.app.get('/user/update')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_user_show(self):
        """"This method tests whether the route '/user/show' succesfully renders a page"""
        indx = self.app.get('/user/show')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_recipe_create(self):
        """"This method tests whether the route '/recipe/create' succesfully renders a page"""
        indx = self.app.get('/recipe/create')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_recipe_update(self):
        """"This method tests whether the route '/recipe/update' succesfully renders a page"""
        indx = self.app.get('/recipe/update')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_users_index(self):
        """"This method tests whether the route '/users' succesfully renders a page"""
        indx = self.app.get('/users')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_index(self):
        """"This method tests whether the route '/recipes/index' succesfully renders a page"""
        indx = self.app.get('/recipes/index')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_index(self):
        """"This method tests whether the route '/recipe/show' succesfully renders a page"""
        indx = self.app.get('/recipe/show')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_index(self):
        """"This method tests whether the route '/recipe/delete' succesfully renders a page"""
        indx = self.app.get('/recipe/delete')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_login(self):
        """Test whether this route renders the a page succesfully"""
        indx = self.app.get('/login')
#Test whether  the route returns HTTP code 200
        self.assertEqual(indx.status_code, 200)

    def test_class_creation(self):
        """This method tests whether an instance of User class can be created succesfully"""
        name = self.user.name
# Test whether user.name returns name as initialized
        self.assertEqual(name, "sam")

    def test_recipe_creation(self):
        """This method tests whether an instance of Recipe class is created succesfully"""
        name = self.recipe.title
# Test whether recipe.title returns name as initialized
        self.assertEqual(name, "recipe example")

    def test_user_count(self):
        """This method tests whether count updates everytime a user is created"""
        count = User.count
        self.assertIsNot(count, 0)

    def test_recipe_count(self):
        """This method tests whether count updates everytime a user is created"""
        count = Recipe.count
        self.assertIsNot(count, 0)

    def test_recipe_id(self):
        """This methods tests whether the set_id method of the recipe class works"""
        id=self.recipe.set_id
        self.assertIsNotNone(id)

    def test_user_id(self):
        """This method tests whether a user id is created for objects of the User class"""
        id=self.user.id
        self.assertIsNotNone(id)

