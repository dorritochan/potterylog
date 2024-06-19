from flask import Blueprint, jsonify, current_app, request
from marshmallow import ValidationError
from urllib.parse import unquote

app = current_app
from app.models import Glaze
from app.schemas import GlazeSchema
from app import db

glaze = Blueprint('glaze', __name__)


@glaze.route('/api/glazes')
def get_glazes():
    
    glazes = Glaze.query.order_by(Glaze.brand, Glaze.brand_id).all()
    glaze_schema = GlazeSchema(many=True)
    try:
        glaze_dict = glaze_schema.dump(glazes)
        return jsonify(glaze_dict)
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'An error occurred' 
        }), 500


@glaze.route('/api/glaze/<int:glaze_id>')
def get_glaze(glaze_id):
    
    glaze = Glaze.query.get_or_404(glaze_id)
    if glaze:
        glaze_schema = GlazeSchema()
        return jsonify(glaze_schema.dump(glaze))
    
    return jsonify({'message': 'Glaze not found'}), 404


@glaze.route('/api/add_glaze', methods=['POST'])
def add_glaze():
    
    data = request.get_json()
    print(data)
    glaze_schema = GlazeSchema(session=db.session)
    
    try:
        new_glaze = glaze_schema.load(data)
        db.session.add(new_glaze)
        db.session.commit()
    
        return jsonify({'message': 'New glaze added!'}), 201
    
    except ValidationError as e:
        print(e)
        return jsonify({'message': e.messages}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500
    

@glaze.route('/api/glaze_brands')
def glaze_brands():
    
    brands = [glaze.brand for glaze in Glaze.query.all()]
    brands = list(dict.fromkeys(brands))
    
    return jsonify(brands)


@glaze.route('/api/glaze_names/<glaze_brand>')
def glaze_names(glaze_brand):
    
    glaze_names = [glaze.name for glaze in Glaze.query.filter(Glaze.brand == glaze_brand)]
    glaze_names = list(dict.fromkeys(glaze_names))
    
    return jsonify(glaze_names)


@glaze.route('/api/glaze_ids/<glaze_brand>')
def glaze_ids(glaze_brand):
    
    glaze_ids = [glaze.brand_id for glaze in Glaze.query.filter(Glaze.brand == glaze_brand)]
    glaze_ids = list(dict.fromkeys(glaze_ids))
    
    return jsonify(glaze_ids)


@glaze.route('/api/glaze_from_name')
def get_glaze_from_brand_name():
    
    glaze_brand = request.args.get('brand')
    glaze_name = request.args.get('name')

    glaze = Glaze.query.filter(Glaze.brand==glaze_brand, Glaze.name==glaze_name).first()
    
    if glaze:
        glaze_schema = GlazeSchema()
        return jsonify(glaze_schema.dump(glaze))
    else:
        return jsonify({'message': 'Glaze not found'}), 404


@glaze.route('/api/glaze_from_id')
def get_glaze_from_brand_id():
    
    glaze_brand = request.args.get('brand')
    glaze_id = request.args.get('brand_id')

    glaze = Glaze.query.filter(Glaze.brand==glaze_brand, Glaze.brand_id==glaze_id).first()
    
    if glaze:
        glaze_schema = GlazeSchema()
        return jsonify(glaze_schema.dump(glaze))
    else:
        return jsonify({'message': 'Glaze not found'}), 404
    
    
@glaze.route('/api/update_glaze/<int:glaze_id>', methods=['PUT'])
def update_glaze(glaze_id):
    
    data = request.get_json()
    print(data)
    old_glaze = Glaze.query.get(glaze_id)
    glaze_schema = GlazeSchema(session=db.session, context={'is_update':True})
    
    if old_glaze:
        # Check if the new values are different from the current ones
        fields = ['brand', 'name', 'brand_id', 'color', 'temp_min', 'temp_max', 'cone', 'glaze_url']
        if all(getattr(old_glaze, field) == data.get(field) for field in fields):
            return jsonify({'message': 'No changes were made.'}), 200
        
        try:
            glaze_schema.load(data, instance=old_glaze, partial=True)
            db.session.commit()
            return jsonify({'message': 'Glaze has been updated!'}), 201
        
        except ValidationError as e:
            print(e)
            return jsonify({'message': e.messages}), 400
            
        except Exception as e:
            print(e)
            return jsonify({'message': e}), 500
            
    else:
        return jsonify({'message': 'Glaze not found.'}), 404
        
        
@glaze.route('/api/delete_glaze/<int:glaze_id>', methods=['DELETE'])
def delete_glaze(glaze_id):
    
    glaze = Glaze.query.get(glaze_id)
    
    if glaze:
        db.session.delete(glaze)
        db.session.commit()
        return jsonify({'message': 'The glaze has been deleted.'}), 201  
    else:      
        return jsonify({'message': 'Glaze not found.'}), 404
        