import  uuid

users_dict={'name':'initial','email':'initia'}


class User(object):

    count=0

    def __init__(self,name,email, password, confirm):
	    User.count+=1
	    self.name=name
	    self.email=email
	    self.password=password
	    self.confirm=confirm


    def set_id(self):
	    self.id=uuid4()



    def add_user(self,name,email):
	    users_dict['name']=name
	    users_dict['email']=email


class Recipe(object):
    count=0


    def __init__(self,title,content):
        self.title=title
        self.content=content


    def set_id(self):
    	self.id=uuid4()



    