from typing import Any
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, validate, ValidationError, validates_schema
from app.models import Clay, Pot, Glaze, PotGlaze
import re

class CustomURLValidator:
    def __init__(self, error=None):
        self.error = error or 'Invalid URL.'
        self.pattern = re.compile(
            r'^(?:http[s]?://)?'  # optional http or https
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __call__(self, value):
        if value is not None:
            if not self.pattern.match(value):
                raise ValidationError(self.error)

            if not value.startswith(('http://', 'https://')):
                return 'https://' + value
        
        return value


class BaseHandlingEmptyString(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) and not value.strip():
            if self.allow_none:
                return None
            else:
                raise ValidationError('Cannot be empty')
        return super()._deserialize(value, attr, data, **kwargs)
    
class IntegerHandlingEmptyString(BaseHandlingEmptyString, fields.Integer):
    pass

class StringHandlingEmptystring(BaseHandlingEmptyString, fields.String):
    pass

class FloatHandlingEmptyString(BaseHandlingEmptyString, fields.Float):
    pass

def range_check_if_not_none(min=None, max=None):
    range_validator = validate.Range(min=min, max=max)
    
    def validator(value):
        if value is not None:
            range_validator(value)
            
    return validator

class PotSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pot
        load_instance = True
        ordered = True
        
    id = fields.Integer(allow_none=True)
    vessel_type = auto_field()
    clay_type = fields.Nested(lambda: ClaySchema(only=('id','clay_name')), attribute="made_with_clay")
    author = auto_field()
    images = auto_field()
    primary_image = auto_field()
    # Throwing
    throw_date = fields.Date()
    throw_weight = IntegerHandlingEmptyString(allow_none=True)
    throw_height = auto_field()
    throw_width = auto_field()
    throw_notes = auto_field()
    # Trimming
    trim_date = fields.Date()
    trim_weight = IntegerHandlingEmptyString(allow_none=True)
    trim_surface_treatment = auto_field()
    trim_notes = auto_field()
    # Bisque firing
    bisque_fire_start = fields.DateTime()
    bisque_fire_program_id = fields.Integer(allow_none=True)
    # bisque_fired_with_program = auto_field()
    bisque_fire_kiln_id = fields.Integer(allow_none=True)
    # bisque_fired_with_kiln = auto_field()
    bisque_fire_end = fields.DateTime()
    bisque_fire_open = fields.DateTime()
    bisque_fire_notes = auto_field()
    # Glazing
    # glaze_date = auto_field()
    used_glazes = fields.Nested(lambda: PotGlazeSchema(only=('glaze', 'number_of_layers', 'display_order')), many=True)
    glaze_notes = auto_field()
    # Glaze firing
    # glaze_fire_start = auto_field()
    glaze_fire_program_id = fields.Integer(allow_none=True)
    # glaze_fired_with_program = auto_field()
    glaze_fire_kiln_id = fields.Integer(allow_none=True)
    glaze_fired_with_kiln = auto_field()
    glaze_fire_end = auto_field()
    glaze_fire_open = auto_field()
    glaze_fire_notes = auto_field()
    
    # commissions = auto_field()
    
    pot_name = fields.Method('get_pot_name')
    
    def get_pot_name(self, obj):
        return obj.get_pot_name()
    

class ClaySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Clay
        load_instance = True  # Optional: deserialize to model instances
        ordered = True
    
    # Define fields explicitly if needed
    id = auto_field()
    brand = StringHandlingEmptystring(allow_none=False, required=True)
    name_id = StringHandlingEmptystring(allow_none=False, required=True)
    color = StringHandlingEmptystring(allow_none=True)
    temp_min = IntegerHandlingEmptyString(allow_none=True)
    temp_max = IntegerHandlingEmptyString(allow_none=True)
    grog_percent = IntegerHandlingEmptyString(allow_none=True, validate=range_check_if_not_none(min=0,max=100))
    grog_size_max = FloatHandlingEmptyString(allow_none=True, validate=range_check_if_not_none(min=0.00, max=10.00))
    url = StringHandlingEmptystring(validate=CustomURLValidator(), allow_none=True)
    pots = fields.List(fields.Nested(PotSchema(only=('id', 'pot_name', 'primary_image'))))
    clay_name = fields.Method('get_clay_name')
    
    def get_clay_name(self, obj):
        return obj.get_clay_name()
    
    @validates_schema
    def validate_existence(self, data, **kwargs):
        brand = data.get('brand')
        name_id = data.get('name_id')
        
        existing_clay = Clay.query.filter_by(brand=brand, name_id=name_id).first()
        if existing_clay:
            raise ValidationError('A clay with this brand and ID already exists.', fields=['brand', 'name_id'])
    

class GlazeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Glaze
        load_instance = True
        ordered = True
        
    id = auto_field()
    glaze_name = fields.Method('get_glaze_name')
    brand = auto_field()
    name = auto_field()
    brand_id = fields.Str()
    color = auto_field()
    temp_min = auto_field()
    temp_max = auto_field()
    cone = auto_field()
    glaze_url = auto_field()
    glazed_pots = fields.Nested(lambda: PotGlazeSchema(only=('pot', 'number_of_layers', 'display_order')), many=True)

    def get_glaze_name(self, obj):
        return obj.get_glaze_name()
    
    
class PotGlazeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PotGlaze
        load_instance = True
        ordered = True
        
    glaze = fields.Nested(GlazeSchema(only=('id','glaze_name')))
    pot = fields.Nested(PotSchema(only=('id', 'primary_image', 'pot_name')))
    number_of_layers = fields.Integer()
    display_order = fields.Integer()