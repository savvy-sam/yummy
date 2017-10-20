from flask import render_template
from flask import request
from wtforms import Form, StringField, TextAreaField, PasswordField , validators

from app import app
from model import User

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
    	form.name.data=User(form.name.data, form.email.data, form.password.data, form.confirm.data)

    return render_template('register.html', form=form)



@app.route('/recipes')
def list():
    return render_template('recipes_index.html')
