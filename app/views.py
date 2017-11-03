"""This file will define the routes in the app and the functions to be executed on that route"""
#import all the variables and definition you will use in the app

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session
from flask import url_for
from functools import wraps
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


def email_uniqueness(email):
    """Checks whether an email is already in use"""
    UserList=[user for user in USERS_INDEX if email == user.email]
    print(">>>  ", len(UserList))
    if len(UserList) == 0:
        return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("login to view this page")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def set_id(anId, aList):
    """This method iterates through a list of objects
    if there is an object whose id matches the parmeter id,
    THe object is assigned to a variable place holder"""
    for item in aList:
        if item.id == anId:
            placeholder= item
            return placeholder


@app.route('/',)
def index():
    """This function will return the index.html when the route is triggered"""
    return render_template('index.html', CATEGORIES=CATEGORIES)

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
            if form.email.data == user.email and form.password.data == user.password:
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
@login_required
def logout():
    if session["logged_in"]:
        session.pop("logged_in")
        session.pop("login_id")
        flash('You have been succesfully logged out!', 'success')
        return redirect('/')
    flash("Already logged in")
    return redirect('/')


class LoginForm(Form):
    """This class will read data from the login form"""
    email = StringField('ENTER EMAIL', [
        validators.DataRequired(message='You need to input your email'), validators.email(message="invalid email")])
    password = PasswordField('ENTER PASSWORD', [
        validators.DataRequired(message='You need to input a password')])

class RegisterForm(Form):
    """This will define a class that reads data from the register form
    The Form parameter is a functionality of wtforms
    """
    name = StringField('NAME', [validators.length(max=20)])
    email = StringField("EMAIL", [validators.length(
        max=20),validators.email(message="invalid email")])
    #email = StringField("EMAIL", [validators.length(
    #   max=20), validators.Regexp('/^\S+@\S+\.\S+$/')])
    password = PasswordField("PASSWORD", [
        validators.DataRequired(), validators.EqualTo('confirm', message="Your passwords do not match")])
    confirm = PasswordField('CONFIRM PASSWORD')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """This function creates an instance of the RegisterForm class
    It reads  the form delivered by requests
    It then creates an instance of the User class from the form data"""
    form = RegisterForm(request.form)
    print(">>>  ", str(form.email.data))
    if request.method == 'POST' and form.validate():
        if email_uniqueness(form.email.data):
#Create an object user of the User class
            global user
            user = User(form.name.data, form.email.data, form.password.data, form.confirm.data)
#Append the object user to the USERS_INDEX list
            global USERS_INDEX
            USERS_INDEX.append(user)
            flash('please log in to continue')
            return redirect('/login')
        flash("This email is already in use")
        return redirect('/')
#re-render the register form if the the post request is not succesful
    return render_template('register.html', form=form)

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        for user in USERS_INDEX:
            print(">>>  ", str(user.id))
            if user.id == id:
                user.name = form.name.data
                user.email = form.email.data
                user.password = form.password.data
                user.confirm =  form.confirm.data
                return redirect('/recipes/index')
#re-render form if the POST request is not succesful
            return 'You are trying to edit a user that doesnt exist'
    return render_template('register.html', form=form,)

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
@login_required
def update_recipe(recipe_id):
    """This function collects data from the register form
    It then updates the user object using data obtained from the form
    """
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        for recipe in RECIPES_INDEX:
            if recipe.id == recipe_id:
                if recipe.user_id == session.get('login_id'):
                    login_id = session['login_id']
                    #recipe = Recipe(form.title.data, form.content.data, login_id)
                    recipe.title = form.title.data
                    recipe.ingridients = form.ingridients.data
                    recipe.category = form.category.data
                    recipe.procedure = form.procedure.data
                    return redirect('/recipes/index')
                flash("are you trying to edit a recipe that doesnt belong to you?")
                return redirect('/recipes/index')
#re-render form if the POST request is not succesful
            flash("You are trying to edit an recipe that doesnt belong to you")
            return redirect('/login') 
    return render_template('recipe.html', form=form)

@app.route('/users')
@login_required
def  people():
    """This function iterates over the users_index list  and returns all users"""
    if len(USERS_INDEX) >= 1:
        for persons in USERS_INDEX:
            return persons.name
    return "sorry No Users in Your App Yet"

@app.route('/recipes/index')
@login_required
def all_recipes():
    """This function iterates over all_recipes list and return all the recipes"""
    if len(RECIPES_INDEX) >= 1:
        for dish in RECIPES_INDEX:
            return render_template('recipes_index.html', recipes=RECIPES_INDEX, user=user, CATEGORIES=CATEGORIES)
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
@login_required
def delete(recipe_id):
    """This function will delete a recipe by removing it from the RECIPES_INDEX list"""
    if len(RECIPES_INDEX) > 0:
        for recipe in RECIPES_INDEX:
                if recipe.user_id == session.get('login_id'):
                    RECIPES_INDEX.remove(recipe)
                    return redirect('/recipes/index') 
                flash("You are trying to delete another user's recipe") 
                return redirect('/recipes/index')  
    flash("There are currently no rrecipes to delete")
    return redirect('/')

@app.route('/user/<int:id>/recipes')
@login_required
#This route returns all recipes belonging to a particular user in a list
def user_recipes(id):
    """list all recipes whose user id is id"""
    alist = [recipe for recipe in RECIPES_INDEX if recipe.user_id == id]
    if len(alist) != 0:
        return render_template('recipes_index.html', recipes=alist, user=user, CATEGORIES=CATEGORIES)
    flash("you do not have any recipes yet") 
    return redirect('/recipes/index')       


class CategoryForm(Form):
    """This creates an object from form data"""
    label= StringField('LABEL', [validators.DataRequired()])
    value= StringField('CATEGORY', [validators.DataRequired()])

@app.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    """This extracts data from the category form and adds it to a list as a tuple """
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        CATEGORIES.append((form.value.data, form.label.data))
        return redirect('/recipe/create')
    return render_template('category_form.html', form=form)

@app.route('/<category>/recipes')
@login_required
def category_recipes(category):
    """returns all recipes whose category is the same as the function parameters"""
    alist = [recipe for recipe in RECIPES_INDEX if recipe.category == category]
    return render_template('recipes_index.html', recipes=alist, user=user, CATEGORIES=CATEGORIES)

@app.route('/<category>/delete')
@login_required
def delete_category(category):
    """deletes a category from the CATEGORIES LISTs"""
    for item in CATEGORIES:
        if item[0] == category:
            CATEGORIES.remove(item)
            return redirect('/')


def correct_user(recipe):
    """Checks whether the signed in user is the owner of the recipe"""
    print(">>>  ", recipe.id)
    recipe.user_id == session.get('login_id')
    print(">>>  ", session.get('login_id'))



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("login to view this page")
            return redirect(url_for('app.login'))
        return f(*args, **kwargs)
    return decorated_function
    