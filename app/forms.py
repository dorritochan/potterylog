from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired
from wtforms.widgets import Input
from app.models import User, Clay

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        '''Check if the username already exists in the database'''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        '''Check if the email already exists in the database'''
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Please use a different email address.')
        

class AddPotForm(FlaskForm):
    vessel_type = StringField('Vessel type', validators=[DataRequired()])
    clay_type = SelectField('Clay type', validators=[InputRequired()], coerce=int, choices=[])
    author = StringField('Author', validators=[DataRequired()])
    throw_date = DateTimeField('Throwing date and time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()], widget=Input(input_type='datetime-local'))
    throw_weight = StringField('Throwing weight in g')
    throw_height = StringField('Throwing heights in cm')
    throw_width = StringField('Throwing widths in cm')
    throw_notes = TextAreaField('Throwing notes')
    trim_date = DateTimeField('Trimming date and time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()], widget=Input(input_type='datetime-local'))
    trim_weight = StringField('Trimmed weight in g')
    trim_surface_treatment = StringField('Surface treatment')
    trim_notes = TextAreaField('Trimming notes')
    submit = SubmitField('Add pot')
        
    def __init__(self, *args, **kwargs):
        super(AddPotForm, self).__init__(*args, **kwargs)
        self.clay_type.choices = [(clay.id, clay.get_name()) for clay in Clay.query.all()]



class AddClayForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    color = StringField('Color')
    temp_min = StringField('Minimum temperature')
    temp_max = StringField('Maximum temperature')
    temp_unit = SelectField('°', coerce=int, choices=[(1, 'C'), (2, 'F')])
    grog_percent = StringField('Grog percentage %')
    grog_size_max = StringField('Grog size mm')
    submit = SubmitField('Add clay')