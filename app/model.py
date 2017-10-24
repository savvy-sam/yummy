"""This model defines two classes User and Recipe"""
#import uuid for generating random ids
import  uuid
from flask import session

class User(object):
    """creates the User class that inherits from object class"""
#defines a count to count the number of objects of Recipe class created
    count = 0

    def __init__(self, name, email, password, confirm):
        """initializes a User object"""
        User.count += 1
        self.name = name
        self.email = email
        self.password = password
        self.confirm = confirm
        self.id=uuid.uuid4()

    def set_id(self):
        """This method create a unique id for User objects
        This method will not be used
        It is an alternative way of creating self.id"""
        self.id = uuid.uuid4()
        return self.id


    def login_user(self):
        """This method saves a user id in the session"""
        session['user_id'] = self.id

    def logged_in(self):
        """This method checks whether the user is logged in
        It does that by checking whether the user id saved in session is the user's id"""
        session.get('user_id') == self.id


class Recipe(object):
    """creates the User class that inherits from object class"""
#defines a count to count the number of objects of Recipe class created
    count = 0

    def __init__(self, title, content):
        """initializes a User object"""
        Recipe.count += 1
        self.title = title
        self.content = content


    def set_id(self):
        """This method create a unique id for User objects"""
        self.id = uuid4()
