from flask import Blueprint, jsonify, current_app, request
from marshmallow import ValidationError

app = current_app
from app.models import Clay
from app.schemas import ClaySchema
from app import db

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
    
    
@clay.route('/api/add_clay', methods=['POST'])
def add_clay():
    
    data = request.get_json()
    print(data)
    clay_schema = ClaySchema(session=db.session)
    
    try:
        new_clay = clay_schema.load(data)
        db.session.add(new_clay)
        db.session.commit()
    
        return jsonify({'message': 'New clay added!'}), 201
    
    except ValidationError as e:
        
        return jsonify({'errors': e.messages}), 400
    

@clay.route('/api/clay_brands')
def clay_brands():
    
    brands = [clay.brand for clay in Clay.query.all()]
    brands = list(dict.fromkeys(brands))
    
    return jsonify(brands)


@clay.route('/api/clay_names/<clay_brand>')
def clay_names(clay_brand):
    
    clay_names = [clay.name_id for clay in Clay.query.filter(Clay.brand == clay_brand)]
    clay_names = list(dict.fromkeys(clay_names))
    
    return jsonify(clay_names)