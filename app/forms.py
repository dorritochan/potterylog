from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Optional
from wtforms.widgets import Input
from app.models import User, Clay, FiringProgram, Kiln, Glaze

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
    clay_type = SelectField('Clay type', validators=[InputRequired()], choices=[])
    author = StringField('Author', validators=[DataRequired()])
    throw_date = DateTimeField('Throwing date and time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()], widget=Input(input_type='datetime-local'))
    throw_weight = StringField('Throwing weight in g')
    throw_height = StringField('Throwing heights in cm')
    throw_width = StringField('Throwing widths in cm')
    throw_notes = TextAreaField('Throwing notes')
    trim_date = DateTimeField('Trimming date and time', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    trim_weight = StringField('Trimmed weight in g')
    trim_surface_treatment = StringField('Surface treatment')
    trim_notes = TextAreaField('Trimming notes')
    bisque_fire_start = DateTimeField('Bisque firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fired_with_program = SelectField('Bisque firing program', choices=[])
    bisque_fired_with_kiln = SelectField('Bisque fired with kiln', choices=[])
    bisque_fire_end = DateTimeField('Bisque firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_notes = TextAreaField('Bisque firing notes')
    glaze_date = DateTimeField('Glazing at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    used_glazes = SelectMultipleField('Used glazes', choices=[], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput(), coerce=int)
    glaze_notes = TextAreaField('Glazing notes')
    glaze_fire_start = DateTimeField('Glaze firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fired_with_program = SelectField('Glaze firing program', choices=[])
    glaze_fired_with_kiln = SelectField('Glaze fired with kiln', choices=[])
    glaze_fire_end = DateTimeField('Glaze firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_notes = TextAreaField('Glaze firing notes')
    submit = SubmitField('Add pot')
        
    def __init__(self, *args, **kwargs):
        super(AddPotForm, self).__init__(*args, **kwargs)
        self.clay_type.choices = [(clay.id, clay.get_name()) for clay in Clay.query.all()]
        self.bisque_fired_with_program.choices = [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Bisque')]
        self.bisque_fired_with_kiln.choices = [(kiln.id, kiln.name) for kiln in Kiln.query.all()]
        self.used_glazes.choices = [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.all()]
        self.glaze_fired_with_program.choices = [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Glaze')]
        self.glaze_fired_with_kiln.choices = [(kiln.id, kiln.name) for kiln in Kiln.query.all()]


class AddClayForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    color = StringField('Color')
    temp_min = StringField('Minimum temperature')
    temp_max = StringField('Maximum temperature')
    temp_unit = SelectField('°', coerce=int, choices=[(1, 'C'), (2, 'F')])
    grog_percent = StringField('Grog percentage %')
    grog_size_max = StringField('Grog size mm')
    submit = SubmitField('Add clay')