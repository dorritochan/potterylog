from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField, TextAreaField, SelectMultipleField, widgets, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Optional, URL
from flask_wtf.file import FileAllowed
from wtforms.widgets import Input
from app.models import User, Clay, FiringProgram, Kiln, Glaze
from datetime import datetime

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
    made_with_clay = SelectField('Clay type', validators=[InputRequired()], choices=[], coerce=int)
    author = StringField('Author', validators=[DataRequired()], default='Dora')
    photo = FileField('Upload photos', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'heic', 'heif'])])
    throw_date = DateTimeField('Throwing date and time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()], widget=Input(input_type='datetime-local'), default=datetime.now)
    throw_weight = StringField('Throwing weight in g')
    throw_height = StringField('Throwing heights in cm')
    throw_width = StringField('Throwing widths in cm')
    throw_notes = TextAreaField('Throwing notes')
    trim_date = DateTimeField('Trimming date and time', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    trim_weight = StringField('Trimmed weight in g')
    trim_surface_treatment = StringField('Surface treatment')
    trim_notes = TextAreaField('Trimming notes')
    bisque_fire_start = DateTimeField('Bisque firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_program_id = SelectField('Bisque firing program', choices=[])
    bisque_fire_kiln_id = SelectField('Bisque fired with kiln', choices=[])
    bisque_fire_end = DateTimeField('Bisque firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_notes = TextAreaField('Bisque firing notes')
    glaze_date = DateTimeField('Glazing at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    used_glazes = SelectMultipleField('Used glazes', choices=[], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput(), coerce=int)
    glaze_notes = TextAreaField('Glazing notes')
    glaze_fire_start = DateTimeField('Glaze firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_program_id = SelectField('Glaze firing program', choices=[])
    glaze_fire_kiln_id = SelectField('Glaze fired with kiln', choices=[])
    glaze_fire_end = DateTimeField('Glaze firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_notes = TextAreaField('Glaze firing notes')
    submit = SubmitField()
    
    def validate_made_with_clay(self, made_with_clay):
        '''Check if the made_with_clay exists in the database'''
        clay = Clay.query.get(made_with_clay.data)
        if clay is None:
            raise ValidationError('There is no such clay with ID {}'.format(made_with_clay))
        
    def validate_bisque_fire_program_id(self, bisque_fire_program_id):
        '''Check if bisque_fire_program_id exists in the database'''
        if FiringProgram.query.get(bisque_fire_program_id.data) is None:
            raise ValidationError('There is no firing program with ID {}'.format(bisque_fire_program_id))
        
    def validate_bisque_fire_kiln_id(self, bisque_fire_kiln_id):
        '''Check if bisque_fire_kiln_id exists in the database'''
        if Kiln.query.get(bisque_fire_kiln_id.data) is None:
            raise ValidationError('There is not kiln with ID {}'.format(bisque_fire_kiln_id))
        
    def validate_used_glazes(self, used_glazes):
        '''Check if used_glazes exist in the database'''
        for glaze in used_glazes:
            if Glaze.query.get(glaze.data) is None:
                raise ValidationError('There is no glaze with ID {}'.format(glaze))
        
    def validate_glaze_fire_program_id(self, glaze_fire_program_id):
        '''Check if glaze_fire_program_id exists in the database'''
        if FiringProgram.query.get(glaze_fire_program_id.data) is None:
            raise ValidationError('There is no firing program with ID {}'.format(glaze_fire_program_id))
        
    def validate_glaze_fire_kiln_id(self, glaze_fire_kiln_id):
        '''Check if glaze_fire_kiln_id exists in the database'''
        if Kiln.query.get(glaze_fire_kiln_id.data) is None:
            raise ValidationError('There is not kiln with ID {}'.format(glaze_fire_kiln_id))
        
    
class AddClayForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    color = StringField('Color')
    temp_min = StringField('Minimum temperature')
    temp_max = StringField('Maximum temperature')
    temp_unit = SelectField('°', coerce=int, choices=[(1, 'C'), (2, 'F')])
    grog_percent = StringField('Grog percentage %')
    grog_size_max = StringField('Grog size mm')
    submit = SubmitField('Add clay')
    
    
class AddGlazeForm(FlaskForm):
    brand = StringField('Brand name', validators=[DataRequired()])
    name = StringField('Glaze name')
    color = StringField('Color')
    temp_min = StringField('Minimum temperature')
    temp_max = StringField('Maximum temperature')
    temp_unit = SelectField('Temperature unit', coerce=int, choices=[(1, '°C'), (2, '°F')])
    brand_id = StringField('Brand ID')
    glaze_url = StringField('Glaze URL', validators=[URL()])
    submit = SubmitField('Add glaze')
    
    