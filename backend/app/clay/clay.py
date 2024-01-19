from flask import Blueprint, jsonify, current_app, request
from marshmallow import ValidationError
from urllib.parse import unquote

app = current_app
from app.models import Clay
from app.schemas import ClaySchema
from app import db

clay = Blueprint('clay', __name__)


@clay.route('/api/clays')
def get_clays():
    
    clays = Clay.query.order_by(Clay.brand, Clay.name_id).all()
    clay_schema = ClaySchema(many=True)
    try:
        clay_dict = clay_schema.dump(clays)
        return jsonify(clay_dict)
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'An error occurred' 
        }), 500
    


@clay.route('/api/clay/<int:clay_id>')
def get_clay(clay_id):
    """
    Show the details of a clay.

    Args:
        clay_id (int): The ID of a clay.

    """
    clay = Clay.query.get(clay_id)
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
        print(e)
        return jsonify({'message': e.messages}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500
    

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


@clay.route('/api/clay')
def get_clay_from_brand_id():
    
    clay_brand = request.args.get('brand')
    clay_name_id = request.args.get('name_id')

    clay = Clay.query.filter(Clay.brand==clay_brand, Clay.name_id==clay_name_id).first()
    
    if clay:
        clay_schema = ClaySchema()
        return jsonify(clay_schema.dump(clay))
    else:
        return jsonify({'message': 'Clay not found'}), 404
    
    
@clay.route('/api/update_clay/<int:clay_id>', methods=['PUT'])
def update_clay(clay_id):
    
    data = request.get_json()
    print(data)
    old_clay = Clay.query.get(clay_id)
    clay_schema = ClaySchema(session=db.session, context={'is_update':True})
    
    if old_clay:
        try:
            clay_schema.load(data, instance=old_clay, partial=True)
            db.session.commit()
            return jsonify({'message': 'Clay has been updated!'}), 201
        
        except ValidationError as e:
            print(e)
            return jsonify({'message': e.messages}), 400
            
        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500
            
    else:
        return jsonify({'message': 'Clay not found.'}), 404
        
        
@clay.route('/api/delete_clay/<int:clay_id>', methods=['DELETE'])
def delete_clay(clay_id):
    
    clay = Clay.query.get(clay_id)
    
    if clay:
        db.session.delete(clay)
        db.session.commit()
        return jsonify({'message': 'The clay has been deleted.'}), 201  
    else:      
        return jsonify({'message': 'Clay not found.'}), 404
        