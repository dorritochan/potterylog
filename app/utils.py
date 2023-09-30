# Utility functions

from app import app
from app.models import Clay, FiringProgram, Kiln, Glaze

from wtforms import validators

import re



def allowed_file(filename):
    """
    Check if the provided file has an allowed extension.

    The function determines the validity of a file's extension by 
    checking it against a predefined list of allowed extensions 
    (stored in app.config['ALLOWED_EXTENSIONS']).

    Args:
        filename (str): Name of the file including its extension.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def set_pot_select_field_choices(form):
    """
    Setting the choices for the select fields on the 'pot' page.

    This function retrieves database objects and shows them as choices
    in respective select fields of the given form. In addition, the first 
    choice is set to (0, '-') for no value chosen.
    
    Args:
        form (FlaskForm): An AddPotForm with all its fields.
    """
    form.made_with_clay.choices = [(0, '-')] + [(clay.id, clay.get_clay_name()) for clay in Clay.query.order_by(Clay.brand, Clay.name_id).all()]
    form.bisque_fire_program_id.choices = [(0, '-')] + [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Bisque')]
    form.bisque_fire_kiln_id.choices = [(0, '-')] + [(kiln.id, kiln.name) for kiln in Kiln.query.order_by(Kiln.name).all()]
    for glaze_form in form.used_glazes:
        glaze_form.glaze.choices = [(0, '-')] + [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.order_by(Glaze.brand, Glaze.brand_id).all()]
    form.glaze_fire_program_id.choices = [(0, '-')] + [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Glaze')]
    form.glaze_fire_kiln_id.choices = [(0, '-')] + [(kiln.id, kiln.name) for kiln in Kiln.query.order_by(Kiln.name).all()]
    

cones = [
        '019', '018', '017', '016', '015', '014', '013', '012', '011',
        '010', '09', '08', '07', '06', '05', '04', '03', '02', '01',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'
        ]
def set_cone_select_field_choices(form):
    
    form.cone.data = [(0, '')] + [(index + 1, cone) for index, cone in enumerate(cones)]

kiln_types = ['Electric', 'Gas']
def set_kiln_type_select_field_choices(form):
    
    form.type.data = [(index + 1, type) for index, type in enumerate(kiln_types)]
    

def get_field_id_or_default(select_field):
    """Return the id of the given field or 0 if it's None."""
    return select_field.id if select_field else 0


def populate_pot_select_field_data(form, pot):
    """Fill in the form data with the values from a given pot."""
    fields_mapping = {
        'made_with_clay': pot.made_with_clay,
        'bisque_fire_program_id': pot.bisque_fired_with_program,
        'bisque_fire_kiln_id': pot.bisque_fired_with_kiln,
        'glaze_fire_program_id': pot.glaze_fired_with_program,
        'glaze_fire_kiln_id': pot.glaze_fired_with_kiln
    }

    for form_field, pot_field in fields_mapping.items():
        form_field_obj = getattr(form, form_field)
        form_field_obj.data = get_field_id_or_default(pot_field)
    
    # Populate glazes
    form_glazes = [glaze.glaze_id for glaze in pot.used_glazes]
    for form_glaze, glaze_id in zip(form.used_glazes.entries, form_glazes):
        form_glaze.glaze.data = glaze_id


def populate_cone_data(form, glaze):
    """Fill in the form data with the values from a given glaze."""
    fields_mapping = {
        'cone': glaze.cone
    }

    for form_field, glaze_field in fields_mapping.items():
        form_field_obj = getattr(form, form_field)
        if glaze_field:
            form_field_obj.data = cones.index(glaze_field) + 1
        else:
            form_field_obj.data = 0
    

def populate_kiln_type_data(form, kiln):
    fields_mapping = {
        'type': kiln.type
    }

    for form_field, type_field in fields_mapping.items():
        form_field_obj = getattr(form, form_field)
        if type_field:
            form_field_obj.data = kiln_types.index(type_field) + 1
        else:
            form_field_obj.data = 0



def safe_query(model, id):
    """
    Retrieve an instance of the given model by its ID, if it exists.

    Given a model and an ID, this function attempts to retrieve the corresponding
    instance from the database. If the provided ID is None or 0 or the instance is not found, 
    the function returns None instead of the instance.

    Args:
        model (db.Model): The database model to query from.
        id (int or str): The ID of the instance to retrieve.

    Returns:
        db.Model or None: The instance with the given ID if it exists; None otherwise.
    """
    return model.query.get(id) if id else None
    
    
def extract_pot_data(form):
    """Extracts data from the AddPotForm form to create a new Pot."""
    
    # Standard pot fields
    pot_form_fields = [
        'author',
        'vessel_type',
        'throw_date',
        'throw_weight',
        'throw_height',
        'throw_width',
        'throw_notes',
        'trim_date',
        'trim_weight',
        'trim_surface_treatment',
        'trim_notes',
        'bisque_fire_start',
        'bisque_fire_program_id',
        'bisque_fire_kiln_id',
        'bisque_fire_end',
        'bisque_fire_open',
        'bisque_fire_notes',
        'glaze_date',
        'glaze_notes',
        'glaze_fire_start',
        'glaze_fire_program_id',
        'glaze_fire_kiln_id',
        'glaze_fire_end',
        'glaze_fire_open',
        'glaze_fire_notes'
    ]
    
    # Standard fields extraction
    data = {field: getattr(form, field).data for field in pot_form_fields}

    # Special field extraction (since it doesn't directly map to a model field)
    data['made_with_clay'] = safe_query(Clay, form.made_with_clay.data) 
    data['bisque_fired_with_program'] = safe_query(FiringProgram, data['bisque_fire_program_id'])
    data['bisque_fired_with_kiln'] = safe_query(Kiln, data['bisque_fire_kiln_id'])
    data['glaze_fired_with_program'] = safe_query(FiringProgram, data['glaze_fire_program_id'])
    data['glaze_fired_with_kiln'] = safe_query(Kiln, data['glaze_fire_kiln_id'])
    
    return data
    

def extract_glaze_data(form):
    """Extracts data from the AddGlazeForm form to create a new Glaze."""
    # Standard fields extraction
    data = {
        'brand': form.brand.data,
        'name': form.name.data,
        'color': form.color.data,
        'temp_min': form.temp_min.data,
        'temp_max': form.temp_max.data,
        'brand_id': form.brand_id.data,
        'glaze_url': form.glaze_url.data
    }
    
    # Special field extraction (since it doesn't directly map to a model field)
    data['cone'] = next(label for value, label in form.cone.choices if value == form.cone.data)

    return data


def extract_clay_data(form):
    """Extracts data from the AddClayForm form to create a new Clay."""
    # Standard fields extraction
    data = {
        'brand': form.brand.data,
        'name_id': form.name_id.data,
        'color': form.color.data,
        'temp_min': form.temp_min.data,
        'temp_max': form.temp_max.data,
        'grog_percent': form.grog_percent.data,
        'grog_size_max': form.grog_size_max.data,
        'url': form.url.data
    }

    return data


def extract_kiln_data(form):
    """Extracts data from the AddKilnForm form to create a new Kiln."""
    # Standard fields extraction
    data = {
        'name': form.name.data,
        'brand': form.brand.data,
        'capacity': form.capacity.data,
        'temp_max': form.temp_max.data,
        'voltage': form.voltage.data,
        'url': form.url.data,
        'controller': form.controller.data,
        'controller_url': form.controller_url.data
    }

    # Special field extraction (since it doesn't directly map to a model field)
    data['type'] = next(label for value, label in form.type.choices if value == form.type.data)

    return data


def extract_firing_segment_data(firing_segment):
    """Extracts data from the FiringSegmentForm form to create a new firing segment."""
    
    data = {
        'temp_start': firing_segment['temp_start'],
        'temp_end': firing_segment['temp_end'],
        'time_to_reach': firing_segment['time_to_reach']
    }

    return data


def extract_link_data(form):
    """Extracts data from the AddLinkForm form to create a new link."""
    
    data = {
        'title': form.title.data,
        'url': form.url.data,
        'description': form.description.data
    }
    
    return data
    

def program_firing_time(firing_program):
    """
    Compute the total firing time for one firing program.

    This helper function takes a FiringProgram instance as an argument 
    and computes the total firing time for it. The firing time of the
    segments of the program are summed up and using divmod splitted into
    hours and minutes for better readability.
    
    Args:
        firing_program (FiringProgram): A FiringProgram instance.
        
    Returns:
        dict: A dictionary containing the keys 'hours' and 'minutes' and
        their respective computed value for the given firing program.
    """
    
    # Retrieve the firing segments of the program
    segments = firing_program.associated_segments
    
    # Compute the sum of the firing times of the segments (in minutes)
    minutes_sum = sum(segment.segment.time_to_reach for segment in segments)
    
    # Split the sum into hours and minutes
    hours, minutes = divmod(minutes_sum, 60)
    
    if hours > 0:
        return '{}h {}min'.format(hours, minutes)
    else:
        return '{}min'.format(minutes)
    
    
def normalize_string(s):
    """Converts the string to lowercase, trims white spaces and replaces multiple spaces with a single space."""
    s = str(s).lower().strip()
    return re.sub(' +', ' ', s)


class CustomURL(object):
    """A custom URL validator for WTForms, which not only accepts urls of 
    the form https://example.com and http://example.com, but also
    example.com"""
    
    def __init__(self, message=None):
        if not message:
            message = u'Invalid URL.'
        self.message = message

    def __call__(self, form, field):
        pattern = re.compile(
            r'^(?:http[s]?://)?'  # optional http or https
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not pattern.match(field.data):
            raise validators.ValidationError(self.message)
        
        # After validation, modify the data if needed
        if not field.data.startswith(('http://', 'https://')):
            field.data = 'https://' + field.data
