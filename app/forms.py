from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from wtforms.fields.html5 import EmailField
from app.models import User

class LoginForm(FlaskForm):
    username_login = StringField(validators=[DataRequired()])
    password_login = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit_login = SubmitField('ВОЙТИ')



class RegisterForm(FlaskForm):
    username_reg = StringField(validators=[DataRequired()])
    email_reg = EmailField(validators=[DataRequired()])
    password_reg = PasswordField(validators=[DataRequired()])
    password_reg2 = PasswordField(validators=[DataRequired(), EqualTo('password_reg')])
    submit_reg = SubmitField('СОЗДАТЬ АККАУНТ')

    def validate_username_reg(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email_reg(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit_search = SubmitField('Поиск')

class CreatePost(FlaskForm):
    title = StringField('Заголовок:', validators=[DataRequired()])
    content = TextAreaField('Текст статьи:', validators=[DataRequired()])
    submit = SubmitField('ДОБАВИТЬ')
