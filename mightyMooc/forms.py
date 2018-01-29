from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo 
from mightyMooc.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(),
		EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		'''
	 	When you add any methods that match the pattern validate_<field_name>, 
	 	WTForms takes those as custom validators and invokes them 
	 	in addition to the stock validators.
		'''
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('User name taken - Try again!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')