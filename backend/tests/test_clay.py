from config import TestConfig
from flask_testing import TestCase
from flask import current_app

app = current_app
from app import db, create_app
from app.models import Clay


class TestClayRoutes(TestCase):
    def create_app(self):
        return create_app(TestConfig)
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_add_clay_valid_data(self):
        # Test with valid data
        response = self.client.post('/api/add_clay', json={
            'brand': 'Test brand',
            'name_id': '123-PC New',
            'color': 'Bright yellow',
            'temp_min': 1000,
            'temp_max': 2300,
            'grog_percent': 15,
            'grog_size_max': 0.1,
            'url': 'https://brand.com/123-PC_new'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('New clay added!', response.json['message'])
        
        new_clay = Clay.query.filter_by(brand='Test brand', name_id='123-PC New').first()
        self.assertIsNotNone(new_clay)
        
    def test_add_clay_invalid_data(self):
        # Test with invalid data
        response = self.client.post('/api/add_clay', json={
            'brand': 'Test brand',
            'name_id': 'DFG-456',
            'color': '123',
            'temp_min': 'foo'
        })
        self.assertEqual(response.status_code, 400)
        # self.assertIn('errors', data)
        # self.assertIn('color', response.json['errors'])