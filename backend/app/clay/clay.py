from flask import Blueprint, jsonify


clay = Blueprint('clay', __name__)

@clay.route('/api/clays')
# @login_required
def get_clays():
    
    clays = Clay.query.order_by(Clay.brand, Clay.name_id).all()
    clay_schema = ClaySchema(many=True)
    
    return jsonify(clay_schema.dump(clays))


@clay.route('/api/clay/<int:clay_id>')
# @login_required
def get_clay(clay_id):
    """
    Show the details of a clay.

    Args:
        clay_id (int): The ID of a clay.

    """
    clay = Clay.query.get_or_404(clay_id)
    
    if clay:
        clay_schema = ClaySchema()
        return jsonify(clay_schema.dump(clay))
    else:
        return jsonify({'message': 'Clay not found'}), 404
    
    
from app.models import Clay
from app.schemas import ClaySchema