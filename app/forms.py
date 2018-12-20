from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields import *
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
  email = EmailField('E-mail', validators=[DataRequired(), Email()])
  password = PasswordField('Пароль', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	email = EmailField('Email', validators=[DataRequired(), Email()])
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			flash('Пользователь с таким именем уже существует.')
			raise ValidationError('Пользователь с таким именем уже существует.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			flash('Пользователь с таким email адрессом уже существует.')
			raise ValidationError('Пользователь с таким email адрессом уже существует.')

class ProfileForm(FlaskForm):
	email = EmailField('Изменить e-mail', validators=[Email()])
	email2 = EmailField('Новый email', validators=[Email()])
	password = PasswordField('Изменить пароль', validators=[])
	password2 = PasswordField('Новый пароль', validators=[])
	submit = SubmitField('Применить')

class NewThemeForm(FlaskForm):
	header = StringField('Название темы', validators=[DataRequired()])
	body = TextAreaField('Описание темы', validators=[DataRequired()])
	submit = SubmitField('Флудануть')

class CommentForm(FlaskForm):
	body = TextAreaField('Комментарий', validators=[DataRequired()])
	submit = SubmitField('Отправить')
