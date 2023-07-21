from app import db 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from pytz import timezone

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
pot_glaze = db.Table('pot_glaze',
    db.Column('pot_id', db.Integer, db.ForeignKey('pot.id')),
    db.Column('glaze_id', db.Integer, db.ForeignKey('glaze.id'))
)  
    
class Pot(db.Model):
    __tablename__ = 'pot'
    # General
    id = db.Column(db.Integer, primary_key=True)
    vessel_type = db.Column(db.String(50))
    clay_type = db.Column(db.Integer, db.ForeignKey('clay.id'), index=True)
    author = db.Column(db.String(30), index=True)
    # Throwing
    throw_date = db.Column(db.DateTime, index=True, default=lambda: germany_timezone.localize(datetime.now()))
    throw_weight = db.Column(db.Integer, index=True)
    throw_weight_unit = db.Column(db.String(10), default='g')
    throw_height = db.Column(db.String(140))
    throw_width = db.Column(db.String(140))
    throw_dimensions_unit = db.Column(db.String(10), default='cm')
    throw_notes = db.Column(db.Text)
    # Trimming
    trim_date = db.Column(db.DateTime, index=True)
    trim_weight = db.Column(db.Integer, index=True)
    trim_weight_unit = db.Column(db.String(10))
    trim_surface_treatment = db.Column(db.String(140), index=True)
    trim_notes = db.Column(db.Text)
    # Bisque firing
    bisque_fire_start = db.Column(db.DateTime, index=True)
    bisque_fire_program_id = db.Column(db.Integer, db.ForeignKey('firing_program.id'), index=True)
    bisque_fired_with_program = db.relationship('FiringProgram', back_populates='bisque_pots', foreign_keys=[bisque_fire_program_id])
    bisque_fire_kiln_id = db.Column(db.Integer, db.ForeignKey('kiln.id'), index=True, default=1)
    bisque_fired_with_kiln = db.relationship('Kiln', back_populates='bisque_fired_pots', foreign_keys=[bisque_fire_kiln_id])
    bisque_fire_end = db.Column(db.DateTime)
    bisque_fire_open = db.Column(db.DateTime)
    bisque_fire_notes = db.Column(db.Text)
    # Glazing
    glaze_date = db.Column(db.DateTime, index=True)
    used_glazes = db.relationship('Glaze', secondary=pot_glaze, back_populates='glazed_pots', lazy='dynamic')
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
    
    def get_glaze_info(self):
        '''This is for displaying purposes for the UI'''
        glaze_info = []
        for glaze in self.used_glazes:
            glaze_info.append(glaze.get_glaze_name())
        return glaze_info 
    
    def get_clay_info(self):
        clay = Clay.query.get(self.clay_type)
        if clay:
            return '{} {} {}{} {}%'.format(clay.brand, clay.color, clay.temp_max, clay.temp_unit, clay.grog_percent)
        return self.clay_type
    
    def __repr__(self):
        return '<Pot {}, {}, {}>'.format(self.throw_date, self.vessel_type, self.clay_type)
    
    
class Glaze(db.Model):
    __tablename__ = 'glaze'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(140), index=True)
    color = db.Column(db.String(140))
    temp_min = db.Column(db.Integer)
    temp_max = db.Column(db.Integer)
    temp_unit = db.Column(db.String(10), default='°C')
    brand_id = db.Column(db.Integer)
    glazed_pots = db.relationship('Pot', secondary=pot_glaze, back_populates='used_glazes', lazy='dynamic')
    
    def get_glaze_name(self):
        return '{} {} {} {}{}'.format(self.brand, self.brand_id, self.color, self.temp_max, self.temp_unit)
    
    def __repr__(self):
        return '<Glaze {}, {}, {}>'.format(self.brand, self.color, self.temp_max)   
    
# Intermediary table for many-to-many relationship between firing segment and firing program
program_segment = db.Table('program_segment',
    db.Column('firing_program_id', db.Integer, db.ForeignKey('firing_program.id')),
    db.Column('firing_segment_id', db.Integer, db.ForeignKey('firing_segment.id'))
)   
    
class FiringProgram(db.Model):
    __tablename__ = 'firing_program'
    id = db.Column(db.Integer, primary_key=True)
    # Bisque or glaze
    type = db.Column(db.String(20))
    name = db.Column(db.String(100))
    associated_segments = db.relationship('FiringSegment', secondary=program_segment, back_populates='associated_programs', lazy='dynamic')
    bisque_pots = db.relationship('Pot', back_populates='bisque_fired_with_program', foreign_keys='[Pot.bisque_fire_program_id]', lazy='dynamic')
    glaze_pots = db.relationship('Pot', back_populates='glaze_fired_with_program', foreign_keys='[Pot.glaze_fire_program_id]', lazy='dynamic')
    
    def __repr__(self):
        return '<Firing program {}>'.format(self.type)  
    
    
class FiringSegment(db.Model):
    __tablename__ = 'firing_segment'
    id = db.Column(db.Integer, primary_key=True)
    temp_start = db.Column(db.Integer)
    temp_end = db.Column(db.Integer)
    temp_unit = db.Column(db.String(10), default='°C')
    time_to_reach = db.Column(db.Integer)
    time_to_reach_unit = db.Column(db.String(10), default='min')
    associated_programs = db.relationship('FiringProgram', secondary=program_segment, back_populates='associated_segments', lazy='dynamic')
    
    def __repr__(self):
        return '<Firing segment {}, {}, {}>'.format(self.temp_start, self.temp_end, self.time_to_reach)  


class Clay(db.Model):
    __tablename__ = 'clay'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(140), index=True)
    color = db.Column(db.String(140))
    temp_min = db.Column(db.Integer)
    temp_max = db.Column(db.Integer)
    temp_unit = db.Column(db.String(10), default='°C')
    grog_percent = db.Column(db.Integer)
    grog_size_max = db.Column(db.Float)
    grog_size_unit = db.Column(db.String(10), default='mm')
    pots = db.relationship('Pot', backref='made_with_clay', lazy='dynamic')
    
    def get_name(self):
        return '{} {} {}{} {}%'.format(self.brand, self.color, self.temp_max, self.temp_unit, self.grog_percent)

    def __repr__(self):
        return '<Clay {}, {}, {}, {}>'.format(self.brand, self.color, self.temp_max, self.grog_percent)   


class Kiln(db.Model):
    __tablename__ = 'kiln'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    brand = db.Column(db.String(140), index=True)
    # Electric or gas
    type = db.Column(db.String(20))
    capacity = db.Column(db.Integer)
    capacity_unit = db.Column(db.String(10), default='L')
    temp_max = db.Column(db.Integer)
    temp_unit = db.Column(db.String(10), default='°C')
    voltage = db.Column(db.String(20))
    controller = db.Column(db.String(200))
    bisque_fired_pots  = db.relationship('Pot', back_populates='bisque_fired_with_kiln', foreign_keys='[Pot.bisque_fire_kiln_id]', lazy='dynamic')
    glaze_fired_pots  = db.relationship('Pot', back_populates='glaze_fired_with_kiln', foreign_keys='[Pot.glaze_fire_kiln_id]', lazy='dynamic')
    
    def __repr__(self):
        return '<Kiln {}>'.format(self.name)