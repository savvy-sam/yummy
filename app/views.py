"""This file will define the routes in the app and the functions to be executed on that route"""
#import all the variables and definition you will use in the app

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from app import app
from app.model import User
from app.model import Recipe

# define empty lists where the users and recipes will be saved after creation
USERS_INDEX = []
RECIPES_INDEX = []


@app.route('/')
def index():
    """This function will return the index.html when the route is triggered"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Tis function will return thr user login form when the route is triggered"""
    return render_template('user_login.html')

@app.route('/signup')
def create():
    """This function will render the registration form when the route is triggered"""
    return render_template('registration_form.html')

class RegisterForm(Form):
    """This will define a class that reads data from the register form
    The Form parameter is a functionality of wtforms
    """
    name = StringField('NAME', [validators.length(max=20)])
    email = StringField("EMAIL", [validators.length(max=20)])
    password = PasswordField("PASSWORD", [validators.DataRequired(), validators.EqualTo('confirm', message="Your passwords do not match")])
    confirm = PasswordField('CONFIRM PASSWORD')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """This function creates an instance of the RegisterForm class
    It reads  the form delivered by requests
    It then creates an instance of the User class from the form data"""
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
#Create an object user of the User class
        user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
#Append the object user to the USERS_INDEX list
        USERS_INDEX.append(user)
        return redirect('/')
        #re-render the register form if the the post request is not succesful
    return render_template('register.html', form=form)

@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        global user
        user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
        return redirect('/')
#re-render form if the POST request is not succesful
    return render_template('register.html', form=form)

@app.route('/recipes')
def listing():
    """This function returns a list of all recipes"""
    return render_template('recipes_index.html')

@app.route('/user/show')
def show_user():
    """This function return a tuple showing the user email and name"""
    return (user.name, user.email)

class RecipeForm(Form):
    """Defines a class RecipeForm that will read data from a html form"""
    title = StringField('TITLE', [validators.length(max=20)])
    content = TextAreaField("CONTENT", [validators.length(max=500)])

@app.route('/create/recipe', methodsss=['GET', 'POST'])
def create_recipe():
    """This function creates an instance of the RecipeForm class
    It reads  the form delivered by requests
    It then creates an instance of the Recipe class from the form data"""
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
# Create an object recipe of the Recipe class
        recipe = Recipe(form.title.data, form.content.data)
# Add recipe object to the list RECIPE_INDEX list
        RECIPES_INDEX.append(recipe)
        return recipe.content
    return render_template('recipe.html', form=form)

@app.route('/recipe/update', methods=['GET', 'POST'])
def update_recipe():
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe = Recipe(form.title.data, form.content.data)
        return recipe.content
#re-render form if the POST request is not succesful
    return render_template('recipe.html', form=form)

@app.route('/users')
def  people():
    """This function iterates over the users_index list  and returns all users"""
    if len(USERS_INDEX) >= 1:
        for persons in USERS_INDEX:
            return persons.name
    return "sorry No Users in Your App Yet"

@app.route('/recipes/index')

def all_recipes():
    """This function iterates over all_recipes list and return all the recipes"""
    if len(RECIPES_INDEX) >= 1:
        for dish in RECIPES_INDEX:
            return dish.name
#flashes a mesage when the recipes_index list is empty
    flash("no users to display yet")
    return redirect('/recipes')
