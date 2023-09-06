# # REST APIs using Flask RESTful

# from flask_restful import Resource, reqparse
# from app.models import Pot  # Import your Pot model

# # Define the Request Parser
# pot_parser = reqparse.RequestParser()
# pot_parser.add_argument('name', type=str, required=True, help='Name field is required')
# pot_parser.add_argument('type', type=str, required=True, help='Type field is required')

# # Define your API Resource
# class PotResource(Resource):
#     def get(self, pot_id):
#         # Retrieve a Pot from the database and serialize it using the schema
#         pot = Pot.query.get(pot_id)
#         return pot_schema.dump(pot)

#     def put(self, pot_id):
#         args = pot_parser.parse_args()  # Parse request data
#         pot = Pot.query.get(pot_id)
#         if not pot:
#             return {'message': 'Pot not found'}, 404
#         pot.name = args['name']
#         pot.type = args['type']
#         db.session.commit()
#         return {'message': 'Pot updated successfully'}
