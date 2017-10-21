from flask import render_template
from flask import request
from flask import redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

from app import app
from app.model import User
from app.model import Recipe
from app.model import recipes_index


users_index = []
recipes_index = []

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
    name = StringField('NAME', [validators.length(max = 20)])
    email = StringField("EMAIL", [validators.length(max = 20)])
    password = PasswordField("PASSWORD", [validators.DataRequired(), 
		                                 validators.EqualTo('confirm', 
		                                 message = "Your passwords do not match")])
    confirm = PasswordField('CONFIRM PASSWORD')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
        #form.populate_obj(user)
        #user.save()

        users_index.append(user)
        user.add_user(user.name, user.email)
        return redirect('/')
        #return user.name    
    return render_template('register.html', form=form)


@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
        #form.populate_obj(user)
        #user.save()
        user.add_user(user.name, user.email)
        return redirect('/')
        #return user.name   
    return render_template('register.html', form=form)





@app.route('/recipes')
def listing():
    return render_template('recipes_index.html')



@app.route('/user/show')
def show_user():
    return (user.name, user.email)



class RecipeForm(Form):
    title = StringField('TITLE', [validators.length(max=20)])
    content = TextAreaField("CONTENT", [validators.length(max=500)])
    

@app.route('/create/recipe', methods = ['GET', 'POST'])
def create_recipe():
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe = Recipe(form.title.data, form.content.data)
        recipes_index.append(recipe)
        return recipe.content
    return render_template('recipe.html', form=form)



@app.route('/recipe/update', methods = ['GET', 'POST'])
def update_recipe():
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe = Recipe(form.title.data, form.content.data)
        return recipe.content
    return render_template('recipe.html', form = form)




@app.route('/users')
def  people():
    if len(users_index) >= 1:
        for persons in users_index:
            return persons.name

    return "sorry No Users in Your App Yet"


@app.route('/recipes/index')

def all_recipes():
    if len(recipes_index) >= 1:
        for dish in recipes_index:
            return dish.name
    return "Dear User , You Dont Have Recipes Here Yet"