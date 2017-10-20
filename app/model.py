import  uuid


class User(object):

    count=0

    def __init__(self,name,password, email, confirm):
	    User.count+=1
	    self.name=name
	    self.email=email
	    self.password=password
	    self.confirm=confirm


    def set_id(self):
	    self.id=uuid4()


