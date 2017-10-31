"""This file will define the routes in the app and the functions to be executed on that route"""
#import all the variables and definition you will use in the app

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from app import app
from app.model import User
from app.model import Recipe

# define empty lists where the users and recipes will be saved after creation
CATEGORIES=[('cakes', 'CAKES'), ('drinks', 'DRINKS'), ('dairy', 'DAIRY'), ('grains', 'GRAINS')]
USERS_INDEX = []
RECIPES_INDEX = []
# declare global variables user and recipe so that they can be used across all methods
user = User("aaaa", "bbbb", 1111, 1111)
recipe=Recipe("aaaa", "bbbb", 123, 'ccc', 'dddd')

@app.route('/')
def index():
    """This function will return the index.html when the route is triggered"""
    return render_template('index.html')

class LoginForm(Form):
    """This class will read data from the login form"""
    email = StringField('ENTER EMAIL',[
        validators.DataRequired(
            message='You need to input your email')])
    password = PasswordField('ENTER PASSWORD', [
        validators.DataRequired(message='You need to input a password')])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This method logs in a user by saving user.id in session"""
    form = LoginForm(request.form)
    if session.get("logged_in"):
        """checks whether the user is already logged in
        If the user is logged in, it redirects and renders a flash message
        """
        flash('You are already logged in')
        redirect('/create/recipe')
    else:
        if request.method == 'POST' or form.validate():
            """reads data from the login form"""
            if form.email.data == user.email or form.password.data == user.password:
                """checks whether the provided data matches user details"""
#save the user id to session.
                session["logged_in"] = True
                session["login_id"] = user.id
                return redirect('recipe/create')
            flash('Password or username incorrect')
            return render_template('user_login.html', form=form)
        return render_template('user_login.html', form=form)
    return render_template('user_login.html', form=form)

@app.route('/logout')
def logout():
    if session["logged_in"]:
        session.pop("logged_in")
        flash('You have been succesfully logged out!', 'success')
        return redirect('login')
    flash("Already logged in")
    return redirect('/')


class LoginForm(Form):
    """This class will read data from the login form"""
    email = StringField('ENTER EMAIL', [
        validators.DataRequired(message='You need to imput your email')])
    password = PasswordField('ENTER PASSWORD', [
        validators.DataRequired(message='You need to imput a password')])

class RegisterForm(Form):
    """This will define a class that reads data from the register form
    The Form parameter is a functionality of wtforms
    """
    name = StringField('NAME', [validators.length(max=20)])
    email = StringField("EMAIL", [validators.length(
        max=20), validators.Regexp(
        '/\S+@\S+\.\S+/', message="Invalid email format")])
    password = PasswordField("PASSWORD", [
        validators.DataRequired(), validators.EqualTo('confirm', message="Your passwords do not match")])
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

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        for user in USERS_INDEX:
            if user.id == id:
                if request.method == 'POST' and form.validate():
                    user.name = form.title.data
                    user.email = form.content.data
                    user.password = form.password.data
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
    flash("no users yet")
    return redirect('/')

class RecipeForm(Form):
    """Defines a class RecipeForm that will read data from a html form"""
    title = StringField('TITLE', [validators.DataRequired(), validators.length(max=20)])
    ingridients = TextAreaField("INGRIDIENTS", [validators.DataRequired(), validators.length(max=500)])
    procedure = TextAreaField("PROCEDURE", [validators.DataRequired(), validators.length(max=500)])
    category = SelectField(u'CATEGORIES', choices=CATEGORIES)
    
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
            recipe = Recipe(form.title.data, form.ingridients.data, form.procedure.data, form.category.data, login_id)
# Add recipe object to the list RECIPE_INDEX list
# RECIPE_INDEX is defined as global so that it can be used in different routes
            global RECIPE_INDEX
            RECIPES_INDEX.append(recipe)
            return redirect('/recipes/index')
        return render_template('recipe.html', form=form)
    flash("you must be logged in to create a recipe")
    return redirect('/login')
@app.route('/recipe/update/<int:recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        for recipe in RECIPES_INDEX:
            if recipe.id == recipe_id:
                    login_id = session['login_id']
                    #recipe = Recipe(form.title.data, form.content.data, login_id)
                    recipe.title = form.title.data
                    recipe.ingridients = form.ingridients.data
                    recipe.category = form.category.data
                    recipe.procedure = form.procedure.data
                    return redirect('/recipes/index')
#re-render form if the POST request is not succesful
            flash("You are trying to edit an recipe that doesnt belong to you")
            return redirect('/login') 
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
            return render_template('recipes_index.html', recipes=RECIPES_INDEX, user=user)
#flashes a mesage when the recipes_index list is empty
    flash("no recipes to display yet")
    return redirect('/recipe/create')

# add a route to show a recipe
@app.route('/recipe/show')

def show_recipe():
    """This function will display the title and contents of a specific recipe"""
    return render_template('show_recipe.html', recipe=recipe)

# add a route to delete a recipe
@app.route('/recipe/delete/<int:recipe_id>')
def delete(recipe_id):
    """This function will delete a recipe by removing it from the RECIPES_INDEX list"""
    if len(RECIPES_INDEX) > 0:
        for recipe in RECIPES_INDEX:
            if recipe.id == recipe_id:
                RECIPES_INDEX.remove(recipe)
                return redirect('/recipes/index')   
            return "The Recipe Does not exist"
    return "no recipes to delete"

@app.route('/user/<int:id>/recipes')
#This route returns all recipes belonging to a particular user in a list
def user_recipes(id):
    """list all recipes whose user id is id"""
    alist = [recipe for recipe in RECIPES_INDEX if recipe.user_id == id]
    if len(alist) != 0:
        return "heheheheheeh"
    return "ooops"


class CategoryForm(Form):
    """This creates an object from form data"""
    label= StringField('LABEL', [validators.DataRequired()])
    value= StringField('CATEGORY', [validators.DataRequired()])

@app.route('/add/category', methods=['GET', 'POST'])
def add_category():
    """This extracts data from the category form and adds it to a list as a tuple """
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        CATEGORIES.append((form.value.data, form.label.data))
        return redirect('/')
    return render_template('category_form.html', form=form)

@app.route('/<category>/recipes')
def category_recipes(category):
    """returns all recipes whose category is the same as the function parameters"""
    alist = [recipe for recipe in RECIPES_INDEX if recipe.category == category]
    return render_template('recipes_index.html', recipes=alist, user=user)

@app.route('/<category>/delete')
def delete_category(category):
    """deletes a category from the CATEGORIES LISTs"""
    for item in CATEGORIES:
        if item[0] == category:
            CATEGORIES.remove(item)
            return redirect('/')


