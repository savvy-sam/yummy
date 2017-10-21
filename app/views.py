from flask import render_template
from flask import request
from flask import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField , validators

from app import app
from model import User
from model import users_dict
from model import Recipe
#user=User('a','b','c','d')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
	return render_template('user_login.html')

@app.route('/signup')
def create():
	return render_template('registration_form.html')



class RegisterForm(Form):
	name=StringField('NAME', [validators.length(max=20)])
	email=StringField("EMAIL", [validators.length(max=20)])
	password=PasswordField("PASSWORD", [validators.DataRequired(), 
		                                validators.EqualTo('confirm', message ="Your passwords do not match")])

	confirm=PasswordField('CONFIRM PASSWORD')


@app.route('/register', methods=['GET', 'POST'] )
def register():
    form=RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user=User(form.name.data, form.email.data, form.password.data, form.confirm.data)
        #form.populate_obj(user)
        #user.save()
        user.add_user(user.name, user.email)
        return redirect('/')
        #return user.name
        
    return render_template('register.html', form=form)



@app.route('/recipes')
def list():
    return render_template('recipes_index.html')



@app.route('/user/show')
def show_user():
	return (user.name, user.email)



class RecipeForm(Form):
    title=StringField('TITLE', [validators.length(max=20)])
    content=TextAreaField("CONTENT", [validators.length(max=500)])
    

@app.route('/create/recipe',methods=['GET','POST'])
def create_recipe():
    form=RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
	    recipe=Recipe(form.title.data, form.content.data)
	    return recipe.content

    return render_template('recipe.html', form=form)



@app.route('/recipe/update', methods=['GET','POST'])
def update_recipe():
    form=RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
	    recipe=Recipe(form.title.data, form.content.data)
	    return recipe.content

    return render_template('recipe.html', form=form)




    

