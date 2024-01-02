from flask import Blueprint, jsonify, current_app

app = current_app
from app.models import Glaze
from app.schemas import GlazeSchema

glaze = Blueprint('glaze', __name__)

@glaze.route('/api/glazes')
# @login_required
def get_glazes():
    
    glazes = Glaze.query.order_by(Glaze.brand, Glaze.brand_id).all()
    glaze_schema = GlazeSchema(many=True)
    
    return jsonify(glaze_schema.dump(glazes))


@glaze.route('/api/glaze/<int:glaze_id>')
def get_glaze(glaze_id):
    
    glaze = Glaze.query.get_or_404(glaze_id)
    if glaze:
        glaze_schema = GlazeSchema()
        return jsonify(glaze_schema.dump(glaze))
    
    return jsonify({'message': 'Glaze not found'}), 404