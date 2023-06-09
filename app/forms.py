from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    code_snippet = TextAreaField('Code Snippet', validators=[Length(min=0, max=5000), DataRequired()])
    code_snippet_lang = StringField('Code Snippet Language', validators=[DataRequired()])
    matching_lang = StringField('Matching Language', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if not email.data.endswith("@illinois.edu"):
            raise ValidationError("Email must end with @illinois.edu")
        
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    code_snippet = TextAreaField('Code Snippet', validators=[Length(min=0, max=5000)])
    code_snippet_lang = StringField('Code Snippet Language', validators=[DataRequired()])
    matching_lang = StringField('Matching Language', validators=[DataRequired()])
    submit = SubmitField('Submit')
