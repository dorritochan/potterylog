# Utility functions and constants
from app import app
from app.models import Clay, FiringProgram, Kiln, Glaze

'''The allowed filenames for the upload of photos'''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


POT_EXCLUDED_FIELDS = ['made_with_clay', 'photo', 'used_glazes', 'submit', 'csrf_token']

def get_pot_fields(form):
    def include_field(field_name):
        return field_name not in POT_EXCLUDED_FIELDS

    return [field_name for field_name, _ in form._fields.items() if include_field(field_name)]

'''Args: model from app.model, id of a certain model item
This function returns the model row with id id if the id is not None. 
Otherwise return None.'''
def safe_query(model, id):
    return model.query.get(id) if id is not None else None


def set_select_field_choices(form):
    form.made_with_clay.choices = [(clay.id, clay.get_name()) for clay in Clay.query.all()]
    form.bisque_fire_program_id.choices = [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Bisque')]
    form.bisque_fire_kiln_id.choices = [(kiln.id, kiln.name) for kiln in Kiln.query.all()]
    form.used_glazes.choices = [(glaze.id, glaze.get_glaze_name()) for glaze in Glaze.query.all()]
    form.glaze_fire_program_id.choices = [(program.id, program.name) for program in FiringProgram.query.filter_by(type='Glaze')]
    form.glaze_fire_kiln_id.choices = [(kiln.id, kiln.name) for kiln in Kiln.query.all()]