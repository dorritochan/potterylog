from flask import Blueprint, jsonify, current_app, request
from marshmallow import ValidationError
from urllib.parse import unquote

app = current_app
from app.models import Link
from app.schemas import LinkSchema
from app import db

link = Blueprint('link', __name__)


@link.route('/api/links')
def get_links():
    
    links = Link.query.order_by(Link.title).all()
    link_schema = LinkSchema(many=True)
    try:
        link_dict = link_schema.dump(links)
        return jsonify(link_dict)
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'An error occurred' 
        }), 500