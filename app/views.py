"""This file will define the routes in the app and the functions to be executed on that route"""
#import all the variables and definition you will use in the app

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from app import app
from app.model import User
from app.model import Recipe

# define empty lists where the users and recipes will be saved after creation
USERS_INDEX = []
RECIPES_INDEX = []
# declare global variables user and recipe so that they can be used across all methods
user = User("aaaa", "bbbb", 1111, 1111)
recipe=Recipe("aaaa", "bbbb", 123)

@app.route('/')
def index():
    """This function will return the index.html when the route is triggered"""
    return render_template('index.html')

class LoginForm(Form):
    """This class will read data from the login form"""
    email = StringField('ENTER EMAIL', [validators.DataRequired(message='You need to imput your email')])
    password = PasswordField('ENTER PASSWORD', [validators.DataRequired(message='You need to imput a password')])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This method logs in a user by saving user.id in session"""
    if session.get("logged_in") == True:
        """checks whether the user is already logged in
        If the user is logged in, it redirects and renders a flash message
        """
        redirect('/create/recipe')
        flask.flash('You are already logged in')
    else:
        form = LoginForm(request.form)
        if request.method == 'POST' or form.validate():
            """reads data from the login form"""
            if form.email.data == user.email or form.password.data == user.password:
                """checks whether the provided data matches user details"""
#save the user id to session.
                session["logged_in"] = True
                session["login_id"] = user.id
                return redirect('recipe/create')
            return "You are entering a wrong password"
        return render_template('user_login.html', form=form)

@app.route('/logout')
def logout():
    if session["logged_in"] == True:
        session.pop("logged_in")
        flash('You have been succesfully logged out!', 'success')
        return redirect('login')
    return "You are not logged in"


class LoginForm(Form):
    """This class will read data from the login form"""
    email = StringField('ENTER EMAIL', [validators.DataRequired(message='You need to imput your email')])
    password = PasswordField('ENTER PASSWORD', [validators.DataRequired(message='You need to imput a password')])

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
        global user
        user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
#Append the object user to the USERS_INDEX list
        global USERS_INDEX
        USERS_INDEX.append(user)

        return redirect('/recipe/create')
        #re-render the register form if the the post request is not succesful
    return render_template('register.html', form=form)

@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        for user in USERS_INDEX:
            if user.id == id:
                if request.method == 'POST' and form.validate():
                    user.name = form.title.data
                    user.email = form.content.data
                    user.password= form.password.data
                    user.confirm =  form.confirm.data
                    return redirect('/recipes/index')
#re-render form if the POST request is not succesful
                return "please submit a form"
            return 'You are trying to edit a user that doesnt exist'
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    return render_template('register.html', form=form)

    

@app.route('/user/show')
def show_user():
    """This function return a tuple showing the user email and name"""
    if user:
        return (user.email, user.email)
    return """No users to display"""

class RecipeForm(Form):
    """Defines a class RecipeForm that will read data from a html form"""
    title = StringField('TITLE', [validators.DataRequired(), validators.length(max=20)])
    content = TextAreaField("CONTENT", [validators.DataRequired(), validators.length(max=500)])

@app.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    """This function creates an instance of the RecipeForm class
    It reads  the form delivered by requests
    It then creates an instance of the Recipe class from the form data"""
    if session.get('logged_in') == True:
        form = RecipeForm(request.form)
        if request.method == 'POST' and form.validate():
# Create an object recipe of the Recipe class
            global recipe
            login_id = session['login_id']
            recipe = Recipe(form.title.data, form.content.data, login_id)
# Add recipe object to the list RECIPE_INDEX list
# RECIPE_INDEX is defined as global so that it can be used in different routes
            global RECIPE_INDEX
            RECIPES_INDEX.append(recipe)
            return redirect('/recipes/index')
        return render_template('recipe.html', form=form)
    return 'login first man'
@app.route('/recipe/update/<int:id>', methods=['GET', 'POST'])
def update_recipe(id):
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        for recipe in RECIPES_INDEX:
            if recipe.id == id:
                if request.method == 'POST' and form.validate():
                    login_id = session['login_id']
                    #recipe = Recipe(form.title.data, form.content.data, login_id)
                    recipe.title = form.title.data
                    recipe.content = form.content.data
                    return redirect('/recipes/index')
#re-render form if the POST request is not succesful
                return "please submit a form"
            return 'You are trying to edit a recipe that doesnt exist'
    return render_template('recipe.html', form=form )

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
            return render_template('recipes_index.html', recipes=RECIPES_INDEX, user=user)
#flashes a mesage when the recipes_index list is empty
    flash("no recipes to display yet")
    return redirect('/recipe/create')

# add a route to show a recipe
@app.route('/recipe/show/<id>')

def show_recipe(id):
    """This function will display the title and contents of a specific recipe"""
    return render_template('show_recipe.html',recipe=recipe)

# add a route to delete a recipe
@app.route('/recipe/delete/<int:id>')
def delete(id):
    """This function will delete a recipe by removing it from the RECIPES_INDEX list"""
    if len(RECIPES_INDEX)>0:
        for recipe in RECIPES_INDEX:
            if recipe.id == id:
                RECIPES_INDEX.remove(recipe)
                return redirect('/recipes/index')   
            return "The Recipe Does not exist"
    return "no recipes to delete"