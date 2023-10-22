from app import db, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from pytz import timezone
from sqlalchemy import event
import os

germany_timezone = timezone('Europe/Berlin')


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    
@login.user_loader
def load_user(id):
    """Loads the user from the database with the id given as argument"""    
    return User.query.get(int(id))

    
# Intermediary table for many-to-many relationship between pot and glaze
class PotGlaze(db.Model):
    __tablename__ = 'pot_glaze'
    
    id = db.Column(db.Integer, primary_key=True)
    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'))
    glaze_id = db.Column(db.Integer, db.ForeignKey('glaze.id'))
    number_of_layers = db.Column(db.Integer)
    display_order = db.Column(db.Integer)
    
    pot = db.relationship('Pot', back_populates='used_glazes')
    glaze = db.relationship('Glaze', back_populates='glazed_pots')
    
class Pot(db.Model):
    __tablename__ = 'pot'
    # General
    id = db.Column(db.Integer, primary_key=True)
    vessel_type = db.Column(db.String(50))
    clay_type = db.Column(db.Integer, db.ForeignKey('clay.id'), index=True)
    author = db.Column(db.String(30), index=True)
    images = db.relationship('Image', back_populates='pot', cascade='all, delete-orphan')
    primary_image = db.Column(db.String(255))
    # Throwing
    throw_date = db.Column(db.Date, index=True, default=lambda: germany_timezone.localize(datetime.now()))
    throw_weight = db.Column(db.Integer, index=True) # in g
    throw_height = db.Column(db.String(140)) # in cm
    throw_width = db.Column(db.String(140)) # in cm
    throw_notes = db.Column(db.Text)
    # Trimming
    trim_date = db.Column(db.Date, index=True)
    trim_weight = db.Column(db.Integer, index=True) # in g
    trim_surface_treatment = db.Column(db.String(140), index=True)
    trim_notes = db.Column(db.Text)
    # Bisque firing
    bisque_fire_start = db.Column(db.Date, index=True)
    bisque_fire_program_id = db.Column(db.Integer, db.ForeignKey('firing_program.id'), index=True)
    bisque_fired_with_program = db.relationship('FiringProgram', back_populates='bisque_pots', foreign_keys=[bisque_fire_program_id])
    bisque_fire_kiln_id = db.Column(db.Integer, db.ForeignKey('kiln.id'), index=True, default=1)
    bisque_fired_with_kiln = db.relationship('Kiln', back_populates='bisque_fired_pots', foreign_keys=[bisque_fire_kiln_id])
    bisque_fire_end = db.Column(db.DateTime)
    bisque_fire_open = db.Column(db.DateTime)
    bisque_fire_notes = db.Column(db.Text)
    # Glazing
    glaze_date = db.Column(db.Date, index=True)
    used_glazes = db.relationship('PotGlaze', back_populates='pot', lazy='dynamic', cascade='all, delete-orphan')
    glaze_notes = db.Column(db.Text)
    # Glaze firing
    glaze_fire_start = db.Column(db.DateTime, index=True)
    glaze_fire_program_id = db.Column(db.Integer, db.ForeignKey('firing_program.id'), index=True)
    glaze_fired_with_program = db.relationship('FiringProgram', back_populates='glaze_pots', foreign_keys=[glaze_fire_program_id])
    glaze_fire_kiln_id = db.Column(db.Integer, db.ForeignKey('kiln.id'), index=True, default=1)
    glaze_fired_with_kiln = db.relationship('Kiln', back_populates='glaze_fired_pots', foreign_keys=[glaze_fire_kiln_id])
    glaze_fire_end = db.Column(db.DateTime, index=True)
    glaze_fire_open = db.Column(db.DateTime, index=True)
    glaze_fire_notes = db.Column(db.Text)
    
    def get_pot_name(self):
        return 'Pot {} {}'.format(self.id, self.vessel_type)
    
    def __repr__(self):
        return '<Pot {}, {}, {}>'.format(self.throw_date, self.vessel_type, self.clay_type)



class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'), nullable=False)
    pot = db.relationship('Pot', back_populates='images')
    
@event.listens_for(Image, 'before_delete')
def delete_image_files(mapper, connection, target):
    """
    Remove the image file associated with the Image object before its record is deleted.
    """
    if target.filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], target.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
            
class Glaze(db.Model):
    __tablename__ = 'glaze'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(140), index=True)
    name = db.Column(db.String(50), unique=True)
    brand_id = db.Column(db.Integer, unique=True)
    color = db.Column(db.String(140))
    temp_min = db.Column(db.Integer) # in °C
    temp_max = db.Column(db.Integer) # in °C
    cone = db.Column(db.String(5))
    glaze_url = db.Column(db.String(200))
    glazed_pots = db.relationship('PotGlaze', back_populates='glaze', lazy='dynamic')
    
    def get_glaze_name(self):
        
        brand = self.brand or ''
        brand_id = self.brand_id or ''
        name = self.name or ''

        return '{} {} {}'.format(brand, brand_id, name)
    
    def __repr__(self):
        return '<Glaze {}, {}, {}>'.format(self.brand, self.color, self.temp_max)   
    
    
# Intermediary table for many-to-many relationship between firing segment and firing program
class ProgramSegment(db.Model):
    __tablename__ = 'program_segment'
    
    program_id = db.Column(db.Integer, db.ForeignKey('firing_program.id'), primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('firing_segment.id'), primary_key=True)
    segment_order = db.Column(db.Integer)
    
    program = db.relationship('FiringProgram', back_populates='associated_segments')
    segment = db.relationship('FiringSegment', back_populates='associated_programs', cascade='all, delete')
    
    
class FiringProgram(db.Model):
    __tablename__ = 'firing_program'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20)) # Bisque or Glaze
    name = db.Column(db.String(100))
    associated_segments = db.relationship('ProgramSegment', back_populates='program', lazy='dynamic', cascade='all, delete-orphan')
    bisque_pots = db.relationship('Pot', back_populates='bisque_fired_with_program', foreign_keys='[Pot.bisque_fire_program_id]', lazy='dynamic')
    glaze_pots = db.relationship('Pot', back_populates='glaze_fired_with_program', foreign_keys='[Pot.glaze_fire_program_id]', lazy='dynamic')
    
    def __repr__(self):
        return '<Firing program {}>'.format(self.name)  
    
    
class FiringSegment(db.Model):
    __tablename__ = 'firing_segment'
    id = db.Column(db.Integer, primary_key=True)
    temp_start = db.Column(db.Integer) # in °C
    temp_end = db.Column(db.Integer) # in °C
    time_to_reach = db.Column(db.Integer) # in min
    associated_programs = db.relationship('ProgramSegment', back_populates='segment', lazy='dynamic', cascade='all')
    
    def __repr__(self):
        return '<Firing segment {}, {}, {}>'.format(self.temp_start, self.temp_end, self.time_to_reach)  


class Clay(db.Model):
    __tablename__ = 'clay'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(140), index=True)
    name_id = db.Column(db.String(140), index=True)
    color = db.Column(db.String(140))
    temp_min = db.Column(db.Integer) # in °C
    temp_max = db.Column(db.Integer) # in °C
    grog_percent = db.Column(db.Integer) # in %
    grog_size_max = db.Column(db.Float) # in mm
    url = db.Column(db.String)
    pots = db.relationship('Pot', backref='made_with_clay', lazy='dynamic')
    
    def get_clay_name(self):
        
        brand = self.brand or ''
        name_id = self.name_id or ''
        color = self.color or ''
        
        return '{} {} {}'.format(brand, name_id, color)

    def __repr__(self):
        return '<Clay {}, {}, {}, {}>'.format(self.brand, self.name_id, self.temp_max, self.grog_percent)   


class Kiln(db.Model):
    __tablename__ = 'kiln'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    brand = db.Column(db.String(140), index=True)
    type = db.Column(db.String(20)) # Electric or Gas
    capacity = db.Column(db.Integer) # in L
    temp_max = db.Column(db.Integer) # in °C
    voltage = db.Column(db.Float(20)) # in kW
    url = db.Column(db.String)
    controller = db.Column(db.String(200))
    controller_url = db.Column(db.String)
    bisque_fired_pots  = db.relationship('Pot', back_populates='bisque_fired_with_kiln', foreign_keys='[Pot.bisque_fire_kiln_id]', lazy='dynamic')
    glaze_fired_pots  = db.relationship('Pot', back_populates='glaze_fired_with_kiln', foreign_keys='[Pot.glaze_fire_kiln_id]', lazy='dynamic')
    
    def __repr__(self):
        return '<Kiln {}>'.format(self.name)
    
    
class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    url = db.Column(db.String)
    description = db.Column(db.String)
    
    def __repr__(self):
        return 'Link {}'.format(self.name)