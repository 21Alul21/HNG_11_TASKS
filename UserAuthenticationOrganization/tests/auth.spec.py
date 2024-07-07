""" moule for testing the application """
import unittest
import pytest
from unittest.mock import patch
from app import app, db
from flask import json
from flask_jwt_extended import decode_token, get_jwt_identity, create_access_token
from app import User, Organisation


# unit testing
class AuthTestCase(unittest.TestCase):
    """ Testcase for Token generation
     and for organisation restriction
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create all tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_token_expiration(self):

        user_data = {
                'firstName': 'Augustine',
                'lastName': 'Alul',
                'email': 'Augustin.alul@yahoo.com',
                'password': 'austine009',
                'phone': '1234567890'
            }
        
        response = self.app.post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('accessToken', data['data'])


    def test_login_user(self):
        # Register a user first
        user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'Password123',
            'phone': '1234567890'
        }
        self.app.post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        
        # Now login with the same user
        login_data = {
            'email': 'john.doe@example.com',
            'password': 'Password123'
        }
        response = self.app.post('/auth/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('accessToken', data['data'])

        # Verify token contains correct user details
        access_token = data['data']['accessToken']
        decoded_token = decode_token(access_token)
        self.assertEqual(decoded_token['sub'], User.query.filter_by(email=user_data['email']).first().userId)
    
    @patch('flask_jwt_extended.view_decorators._decode_jwt_from_request')
    def test_token_expiration(self, mock_decode_jwt_from_request):
        user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'Password123',
            'phone': '1234567890'
        }
        response = self.app.post('/auth/register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('accessToken', data['data'])

        # Mock the token as expired
        expired_token = create_access_token(identity=user_data['email'], expires_delta=-1)  # Immediately expired token
        mock_decode_jwt_from_request.return_value = decode_token(expired_token)

        # Attempt to use the expired token
        headers = {'Authorization': f'Bearer {expired_token}'}
        protected_response = self.app.get('/protected', headers=headers)
        self.assertEqual(protected_response.status_code, 401)



# end to end testing
@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def register_user(client, user_data):
    return client.post('/auth/register', data=json.dumps(user_data), content_type='application/json')

def login_user(client, login_data):
    return client.post('/auth/login', data=json.dumps(login_data), content_type='application/json')

def test_user_registration(client):
    # Test user registration success
    user_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "password123",
        "phone": "1234567890"
    }
    
    response = register_user(client, user_data)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert 'accessToken' in data['data']
    assert data['data']['user']['firstName'] == user_data['firstName']
    assert data['data']['user']['lastName'] == user_data['lastName']
    assert data['data']['user']['email'] == user_data['email']

    # Verify default organisation name
    organisation = Organisation.query.filter_by(name="John's Organisation").first()
    assert organisation is not None

def test_user_registration_validation(client):
    # Test user registration validation errors
    user_data = {
        "firstName": "",
        "lastName": "Doe",
        "email": "johndoeexample.com",
        "password": "123",
        "phone": "phone"
    }
    
    response = register_user(client, user_data)
    assert response.status_code == 422
    data = response.get_json()
    assert len(data['errors']) > 0

def test_duplicate_email_registration(client):
    # Test duplicate email registration
    user_data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "janedoe@example.com",
        "password": "password123",
        "phone": "0987654321"
    }
    
    response1 = register_user(client, user_data)
    response2 = register_user(client, user_data)

    assert response1.status_code == 201
    assert response2.status_code == 422
    data = response2.get_json()
    assert data['errors'][0]['field'] == 'email'
    assert data['errors'][0]['message'] == 'email address already exist'

def test_user_login_success(client):
    # Test user login success
    user_data = {
        "firstName": "Jake",
        "lastName": "Smith",
        "email": "jakesmith@example.com",
        "password": "password123",
        "phone": "1234509876"
    }

    # Register user first
    register_user(client, user_data)

    login_data = {
        "email": "jakesmith@example.com",
        "password": "password123"
    }

    response = login_user(client, login_data)
    data = response.get_json()
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert 'accessToken' in data['data']
    assert data['data']['user']['firstName'] == user_data['firstName']
    assert data['data']['user']['lastName'] == user_data['lastName']
    assert data['data']['user']['email'] == user_data['email']

def test_user_login_failure(client):
    # Test user login failure
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = login_user(client, login_data)
    data = response.get_json()

    assert response.status_code == 401
    assert data['status'] == 'Bad request'
    assert data['message'] == 'Authentication failed'


if __name__ == '__main__':
    unittest.main()
