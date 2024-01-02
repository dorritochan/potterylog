from flask import Blueprint, jsonify, current_app, request
from sqlalchemy import desc

app = current_app

from app.models import Pot
from app.schemas import PotSchema
from app import db

pot = Blueprint('pot', __name__)

@pot.route('/api/pots')
# @login_required
def get_pots():
    
    pots = Pot.query.order_by(desc(Pot.id)).all()
        
    pots_schema = PotSchema(many=True, only=('id', 'primary_image', 'throw_date', 'vessel_type', 'clay_type', 'used_glazes'))
    
    return jsonify(pots_schema.dump(pots))


@pot.route('/api/pot/<int:pot_id>')
def get_pot(pot_id):
    
    pot = Pot.query.get_or_404(pot_id)
    
    if pot:
        pot_schema = PotSchema()
        return jsonify(pot_schema.dump(pot))
    
    return jsonify({'message': f'Pot with id {pot_id} not found'}), 404


@pot.route('/api/add_pot', methods=['POST'])
def add_pot():
    
    data = request.get_json()
    pot = Pot(
        
    )
    
    db.session.add(pot)
    db.session.commit()
    
    return jsonify({'message': 'New pot added!'}), 201