# Utility functions and constants
from app import app
from app.models import Clay, FiringProgram, Kiln, Glaze

'''The allowed filenames for the upload of photos'''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


POT_EXCLUDED_FIELDS = ['made_with_clay', 'photos', 'used_glazes', 'submit', 'csrf_token']
'''Save the form.<field_name>.data to <field_name>, exclude POT_EXCLUDED_FIELDS'''
def get_pot_fields(form):
    def include_field(field_name):
        return field_name not in POT_EXCLUDED_FIELDS

    return [field_name for field_name, _ in form._fields.items() if include_field(field_name)]

'''Args: model from app.model, id of a certain model item
This function returns the model row with id id if the id is not None. 
Otherwise return None.'''
def safe_query(model, id):
    return model.query.get(id) if id and id is not '-1' else None


def set_select_field_choices(form):
    form.made_with_clay.choices = [('-1', '-')] + [(clay.id, clay.get_clay_name()) for clay in Clay.query.all()]
    form.bisque_fire_program_id.choices = [('-1', '-')] + [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Bisque')]
    form.bisque_fire_kiln_id.choices = [('-1', '-')] + [(kiln.id, kiln.name) for kiln in Kiln.query.all()]
    for glaze_form in form.used_glazes:
        glaze_form.glaze.choices = [('-1', '-')] + [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.all()]
    form.glaze_fire_program_id.choices = [('-1', '-')] + [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Glaze')]
    form.glaze_fire_kiln_id.choices = [('-1', '-')] + [(kiln.id, kiln.name) for kiln in Kiln.query.all()]
    

def prepopulate_select(pot_select_field):
    if pot_select_field:
        return pot_select_field.id
    else:
        return -1
    
    
    

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
    data['temp_unit'] = next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data)

    return data


def extract_clay_data(form):
    """Extracts data from the AddClayForm form to create a new Clay."""
    # Standard fields extraction
    data = {
        'brand': form.brand.data,
        'color': form.color.data,
        'temp_min': form.temp_min.data,
        'temp_max': form.temp_max.data,
        'grog_percent': form.grog_percent.data,
        'grog_size_max': form.grog_size_max.data
    }

    # Special field extraction (since it doesn't directly map to a model field)
    data['temp_unit'] = next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data)

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
        'controller': form.controller.data
    }

    # Special field extraction (since it doesn't directly map to a model field)
    data['type'] = next(label for value, label in form.type.choices if value == form.type.data)
    data['temp_unit'] = next(label for value, label in form.temp_unit.choices if value == form.temp_unit.data)

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