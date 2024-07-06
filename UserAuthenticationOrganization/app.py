from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_manager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Organization
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb'

db.init_app(app)


@app.route('/auth/register', methods=['POST'], strict_slashes=False)
def register_user():
    """ view for handling user registeration """
    user_info = request.get_json
   
    if user_info:
        firstName = user_info.get('firstName')
        lastName = user_info.get('lastName')
        email = user_info.get('email')
        password = user_info.get('password')
        phone = user_info.get('phone')


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
        
        if '@' and '.' not in email:
                  return jsonify({
                'errors': [
                    {'field': 'email',
                     'message': 'invalid email address'
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
        
        if not password.isalphanumeric():
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
                  
        if phone.isalphanumeric():
             return jsonify({
                'errors': [
                    {'field': 'phone',
                     'message': 'invalid input, phone field must not contain alphabets'
                     }
                ]                
            }), 422
                  
        
              

        
        pw_salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), pw_salt)


        

         
         
        
if __name__ == '__main__':
    app.run(debug=True)
