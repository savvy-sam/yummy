"""This model defines two classes User and Recipe"""
#import uuid for generating random ids
import  uuid

class User(object):
    """creates the User class that inherits from object class"""
#defines a count to count the number of objects of Recipe class created
    count=0

    def __init__(self, name, email, password, confirm):
        """initializes a User object"""   
        User.count+=1
        self.name=name
        self.email=email
        self.password=password
        self.confirm=confirm

    
    def set_id(self):
        """This method create a unique id for User objects"""
        self.id=uuid4()


class Recipe(object):
    """creates the User class that inherits from object class"""
#defines a count to count the number of objects of Recipe class created
    count=0


    def __init__(self,title,content):
        """initializes a User object""" 
    	Recipe.count+=1
        self.title=title
        self.content=content


    def set_id(self):
        """This method create a unique id for User objects"""
    	self.id=uuid4()



