from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, DateTimeField, 
    SelectField, TextAreaField, SelectMultipleField, widgets, MultipleFileField, 
    IntegerField, FormField, FieldList, FloatField, DateField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired, Optional, URL
from wtforms.widgets import Input

from datetime import datetime

from app.models import User, Clay, FiringProgram, Kiln, Glaze
from app.utils import (
    normalize_string, CustomURL, 
    set_cone_choices, set_kiln_type_choices, set_firing_program_type_choices
)


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
        
class GlazeLayerForm(FlaskForm):
    glaze = SelectField('Glaze', coerce=int)
    number_of_layers = IntegerField('Number of Layers', default=1)

class AddPotForm(FlaskForm):
    vessel_type = StringField('Vessel type', validators=[DataRequired()])
    made_with_clay = SelectField('Clay', validators=[InputRequired()], choices=[], coerce=int)
    author = StringField('Author', validators=[DataRequired()], default='Dora')
    photos = MultipleFileField('Upload photos', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'heic', 'heif'])])
    throw_date = DateField('Throwing date', format='%Y-%m-%d', validators=[DataRequired()], widget=Input(input_type='date'), default=datetime.now)
    throw_weight = StringField('Throwing weight') 
    throw_height = StringField('Throwing heights')
    throw_width = StringField('Throwing widths')
    throw_notes = TextAreaField('Throwing notes')
    trim_date = DateField('Trimming date', format='%Y-%m-%d', widget=Input(input_type='date'), validators=[Optional()])
    trim_weight = StringField('Trimmed weight')
    trim_surface_treatment = StringField('Surface treatment')
    trim_notes = TextAreaField('Trimming notes')
    bisque_fire_start = DateTimeField('Bisque firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_program_id = SelectField('Bisque firing program', choices=[], coerce=int)
    bisque_fire_kiln_id = SelectField('Bisque fired with kiln', choices=[], coerce=int)
    bisque_fire_end = DateTimeField('Bisque firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    bisque_fire_notes = TextAreaField('Bisque firing notes')
    glaze_date = DateField('Glazing date', format='%Y-%m-%d', widget=Input(input_type='date'), validators=[Optional()])
    used_glazes = FieldList(FormField(GlazeLayerForm), min_entries=1)
    glaze_notes = TextAreaField('Glazing notes')
    glaze_fire_start = DateTimeField('Glaze firing started at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_program_id = SelectField('Glaze firing program', choices=[], coerce=int)
    glaze_fire_kiln_id = SelectField('Glaze fired with kiln', choices=[], coerce=int)
    glaze_fire_end = DateTimeField('Glaze firing ended at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_open = DateTimeField('Kiln opened at', format='%Y-%m-%dT%H:%M', widget=Input(input_type='datetime-local'), validators=[Optional()])
    glaze_fire_notes = TextAreaField('Glaze firing notes')
    submit = SubmitField()
    
    def validate_made_with_clay(self, made_with_clay):
        '''Check if the made_with_clay exists in the database'''
        if made_with_clay.data > 0:
            if Clay.query.get(made_with_clay.data) is None:
                raise ValidationError('There is no such clay with ID {}'.format(made_with_clay.data))
        
    def validate_bisque_fire_program_id(self, bisque_fire_program_id):
        '''Check if bisque_fire_program_id exists in the database'''
        if bisque_fire_program_id.data > 0:
            if FiringProgram.query.get(bisque_fire_program_id.data) is None:
                raise ValidationError('There is no firing program with ID {}'.format(bisque_fire_program_id.data))
        
    def validate_bisque_fire_kiln_id(self, bisque_fire_kiln_id):
        '''Check if bisque_fire_kiln_id exists in the database'''
        if bisque_fire_kiln_id.data > 0:
            if Kiln.query.get(bisque_fire_kiln_id.data) is None:
                raise ValidationError('There is not kiln with ID {}'.format(bisque_fire_kiln_id.data))
        
    def validate_used_glazes(self, used_glazes):
        '''Check if used_glazes exist in the database'''
        for glaze in used_glazes:
            glaze_id = glaze.data.get('glaze')
            if glaze_id > 0:
                if Glaze.query.get(glaze_id) is None:
                    raise ValidationError('There is no glaze with ID {}'.format(glaze_id))
        
    def validate_glaze_fire_program_id(self, glaze_fire_program_id):
        '''Check if glaze_fire_program_id exists in the database'''
        if glaze_fire_program_id.data > 0:
            if FiringProgram.query.get(glaze_fire_program_id.data) is None:
                raise ValidationError('There is no firing program with ID {}'.format(glaze_fire_program_id.data))
        
    def validate_glaze_fire_kiln_id(self, glaze_fire_kiln_id):
        '''Check if glaze_fire_kiln_id exists in the database'''
        if glaze_fire_kiln_id.data > 0:
            if Kiln.query.get(glaze_fire_kiln_id.data) is None:
                raise ValidationError('There is not kiln with ID {}'.format(glaze_fire_kiln_id.data))
        
    
class AddClayForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired()])
    name_id = StringField('Name or ID', validators=[DataRequired()])
    color = StringField('Color')
    temp_min = IntegerField('Minimum temperature °C', validators=[Optional()])
    temp_max = IntegerField('Maximum temperature °C', validators=[Optional()])
    grog_percent = IntegerField('Grog percentage %', validators=[Optional()])
    grog_size_max = FloatField('Grog size mm', validators=[Optional()])
    url = StringField('URL', validators=[Optional(), CustomURL()])
    submit = SubmitField('Add clay')
    
    
class AddGlazeForm(FlaskForm):
    brand = StringField('Brand name', validators=[DataRequired()])
    name = StringField('Glaze name', validators=[DataRequired()])
    brand_id = StringField('Brand ID')
    color = StringField('Color')
    temp_min = IntegerField('Minimum temperature °C', validators=[Optional()])
    temp_max = IntegerField('Maximum temperature °C', validators=[Optional()])
    cone = SelectField('Cone', choices=[], coerce=int)
    glaze_url = StringField('Glaze URL', validators=[Optional(), CustomURL()])
    submit = SubmitField('Add glaze')
    
    
    def __init__(self, *args, **kwargs):
        super(AddGlazeForm, self).__init__(*args, **kwargs)
        self.cone.choices = set_cone_choices()
    
class AddKilnForm(FlaskForm):
    name = StringField('Kiln name')
    brand = StringField('Brand name', validators=[DataRequired()])
    type = SelectField('Type', coerce=int)
    capacity = IntegerField('Capacity L', validators=[Optional()])
    temp_max = IntegerField('Maximum temperature °C', validators=[Optional()])
    voltage = FloatField('Voltage kW', validators=[Optional()])
    url = StringField('URL', validators=[Optional(), CustomURL()])
    controller = StringField('Controller')
    controller_url = StringField('Controller URL', validators=[Optional(), CustomURL()])
    submit = SubmitField('Add kiln')
    
    def __init__(self, *args, **kwargs):
        super(AddKilnForm, self).__init__(*args, **kwargs)
        self.type.choices = set_kiln_type_choices()
    

class FiringSegmentForm(FlaskForm):
    temp_start = IntegerField('Start temperature °C', validators=[Optional()])
    temp_end = IntegerField('End temperature °C', validators=[Optional()])
    time_to_reach = IntegerField('Time to reach (min)', validators=[Optional()], default=0)
    
    def __init__(self, *args, **kwargs):
        self.is_first_segment = kwargs.pop('is_first_segment', False)
        super(FiringSegmentForm, self).__init__(*args, **kwargs)
    
    # def validate_temp_fields(form):
    #     if not form.temp_start.data and not form.temp_end.data:
    #         raise ValidationError('Both start and end temperatures are required for this segment.')
    
    
class AddFiringProgramForm(FlaskForm):
    type = SelectField('Type', coerce=int)
    name = StringField('Name')
    firing_segments = FieldList(FormField(FiringSegmentForm), min_entries=1)
    submit = SubmitField('Add program')
    
    def __init__(self, *args, **kwargs):
        super(AddFiringProgramForm, self).__init__(*args, **kwargs)
        self.type.choices = set_firing_program_type_choices()
        
    def validate_firing_segments(form, field):
        first_segment = field.entries[0]
        
        if not first_segment.form.temp_start.data and not first_segment.form.temp_end.data:
            first_segment.form.temp_start.errors.append('Both start and end temperatures are required for the first segment.')
            raise ValidationError('Both start and end temperatures are required for the first segment.')
    
class AddLinkForm(FlaskForm):
    title = StringField('Title')
    url = StringField('URL', validators=[Optional(), CustomURL()])
    description = TextAreaField('Description')
    submit = SubmitField('Add link')
    
    
class AddCommissionForm(FlaskForm):
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()], widget=Input(input_type='date'))
    commissioner = StringField('Commissioner', validators=[DataRequired()])
    object = StringField('Object', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[Optional()], default=1)
    description = TextAreaField('Description')
    done = BooleanField('Done', default=False)
    
    submit = SubmitField('Add commission')