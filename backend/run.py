from app import create_app, db
from app.models import Pot, Glaze, Kiln, Clay, FiringProgram, FiringSegment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Pot': Pot, 'Glaze': Glaze, 'Kiln': Kiln, 'Clay': Clay, 'FiringProgram': FiringProgram, 'FiringSegment': FiringSegment}
