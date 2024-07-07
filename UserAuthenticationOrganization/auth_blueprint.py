""" module containing the authentication logic """

import uuid
from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Organisation
import bcrypt
from models import db

auth = Blueprint(name='authentication', url_prefix='/auth', import_name=__file__)

JWT = JWTManager()


@auth.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    """ view for handling user registeration """

    
    user_info = request.get_json
   
    if user_info:
        firstName = request.json.get('firstName')
        lastName = request.json.get('lastName')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')


        #validating input fields

        # firstname field validation
        if firstName is None:
            return jsonify({
                'errors': [
                    {'field': 'firstName',
                     'message': 'First name field cannot be blank'
                     }
                ]                
            }), 422
        
        if len(firstName) >= 20:
            return jsonify({
                'errors': [
                    {'field': 'firstName',
                     'message': 'First name is too long, it shoulbe less than 20'
                     }
                ]     
            }), 422
        

        # last name field validation
        if lastName is None:
            return jsonify({
                'errors': [
                    {'field': 'lastName',
                     'message': 'last name field cannot be blank'
                     }
                ]                
            }), 422
        
        if len(lastName) >= 20:
            return jsonify({
                'errors': [
                    {'field': 'lasttName',
                     'message': 'last name is too long, it shoulbe less than 20'
                     }
                ]     
            }), 422
        
        # email field validation
        if email is None:
            return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'email field cannot be blank'
                     }
                ]                
            }), 422
        
        if '@' not in email or '.' not in email:
                  return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'invalid email address'
                     }
                ]                
            }), 422
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
             return jsonify({
                  'errors': [
                    {'field': 'email',
                     'message': 'email address already exist'
                     }
                  ]
             }), 422

        
        # password field validation
        if not password:
                   return jsonify({
                'errors': [
                    {'field': 'password',
                     'message': 'password field cannot be blank'
                     }
                ]                
            }), 422
        
        if password.isnumeric():
             return jsonify({
                'errors': [
                    {'field': 'password',
                     'message': 'password field must contain both numbers and characters'
                     }
                ]                
            }), 422
        
        if len(password) < 4:
             return jsonify({
                'errors': [
                    {'field': 'password',
                     'message': 'password is too short'
                     }
                ]                
            }), 422
        
        # phone number field validation
        if not phone:
             return jsonify({
                'errors': [
                    {'field': 'phone',
                     'message': 'phone field must contain both numbers and characters'
                     }
                ]                
            }), 422
                  
        if not phone.isnumeric():
             return jsonify({
                'errors': [
                    {'field': 'phone',
                     'message': 'invalid input, phone field must not contain alphabets'
                     }
                ]                
            }), 422
        
        # hashing the user's password
        pw_salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), pw_salt)
        user = User(firstName=firstName, lastName=lastName, email=email, password=hashed_pw, phone=phone, userId=str(uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.userId)

        # creating default organisation register
        name = firstName + 's' + ' Organisation'
        organisation = Organisation(name=name, description='', orgId=str(uuid.uuid4()))
        db.session.add(organisation)
        db.session.commit()

        user.organisations.append(organisation)

        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                  'accessToken': access_token,
                  'user': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                   }
            }
        }), 201
    
    return jsonify({
          'status': 'Bad request',
          'message': 'Registration unsuccessful',
          'statusCode': 400
    }), 400


@auth.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
     """ view function that handles user login """

     user_info = request.get_json
     if user_info:
        email = request.json.get('email')
        password = request.json.get('password')

        # email validation
        if not email:
             return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'email field cannot be blank'
                     }
                ]                
            }), 422
        
        if not '@' or not '.' in email:
                  return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'invalid email address'
                     }
                ]                
            }), 422
        
        user = User.query.filter_by(email=email).first()
             
        if not user.email:
             return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'invalid input, invalid email address'
                     }
                ]                
            }), 422
        

        # password validation
        if not password:
                   return jsonify({
                'errors': [
                    {'field': 'password',
                     'message': 'password field cannot be blank'
                     }
                ]                
            }), 422
        
        if password.isnumeric():
             return jsonify({
                'errors': [
                    {'field': 'password',
                     'message': 'password field must contain both numbers and characters'
                     }
                ]                
            }), 422
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
              access_token = create_access_token(identity=user.userId)
              return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': access_token,
                    'user': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                   }
                }
            }), 201
        
        else:
              return jsonify({
          'status': 'Bad request',
          'message': 'Authentication failed',
          'statusCode': 401
    }), 401
        