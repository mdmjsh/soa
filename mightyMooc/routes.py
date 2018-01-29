'''
So what goes in the routes module? The routes are the different URLs that the application implements.
In Flask, handlers for the application routes are written as Python functions, called view functions. 
View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.


 A common pattern with decorators is to use them to register functions as callbacks for certain events. 
 In this case, the @app.route decorator creates an association between the URL given as an argument and the function. 
In this example there are two decorators, which associate the URLs / and /index to this function.


'''
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from mightyMooc import app, db
from mightyMooc.models import User
from mightyMooc.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',  title='Welcome to the Jungle')


@app.route('/login', methods=['GET', 'POST'])
def login():

	'''
	The current_user variable comes from Flask-Login and can be used 
	at any time during the handling to obtain the user object that 
	represents the client of the request. 
	'''
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password') # flask flash message
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		
		'''
		The @login_required decorator will intercept 
		the request and respond with a redirect to /login,
		but it will add a query string argument to this URL,
		making the complete redirect URL /login?next=/index. 
		The next query string argument is set to the original URL, 
		so the application can use that to redirect back after login.
		'''
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	# 
	logout_user()  # Flask-Login's logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congrats! You\'re a user bruv!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'},
	]
	return render_template('user.html', user=user, posts=posts)

	



















