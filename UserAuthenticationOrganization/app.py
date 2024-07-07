""" module containing the main application instance """

import os
import datetime
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, User, Organisation
import bcrypt
from auth_blueprint import JWT, auth
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb'
# app.config['JWT_SECRET_KEY'] = 'jhbdwbhqwibcqbcqobcqocq'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)



app.register_blueprint(auth)

db.init_app(app)
JWT.init_app(app)

     
@app.route('/api/users/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def user_record(id):
      
      """ view that returns the user's record in organisations
        they belong to or created 
      """

      user = User.query.get(id)
      if not user:
           return jsonify({
                         'errors': [
                              {'field': 'userId',
                              'message': 'please enter a valid userId'
                              }
                         ]     
                    }), 422
      return jsonify(
           {
                'status': 'success',
                'message': 'user details',
                'data': {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone
                }
            }), 200


@app.route('/api/organisations', methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def organisations():
     """ view that returns all organisations that a user 
     belongs to or created 
     """
     if request.method == 'GET':
          current_user_id = get_jwt_identity()
          user = User.query.get(current_user_id)
          user_organisations = user.organisations

          user_organisations_list = [{ 'orgId': org.orgId,
                                   'name': org.name,
                                   'description': org.description,
                                   } 
                                   for org in user_organisations]
          return jsonify({
          'status': 'success',
          'message': 'user organisations',
          'data': {
               'organisations': user_organisations_list
          }
          }), 200
     
     elif request.method == 'POST':
          # handle users creating of new organisations 
          try:

               current_userId = get_jwt_identity()
               name = request.json.get('name')
               description = request.json.get('description')

               if not name:
                    return jsonify({
                         'errors': [
                              {'field': 'name',
                              'message': 'name field cannot be blank'
                              }
                         ]     
                    }), 422
               user = User.query.get(current_userId)
          
               organisation = Organisation(name=name, description=description)
               db.session.add(organisation)
               db.session.commit()

               # associating the user with the newly created organisation object
               user.organisations.append(organisation)

               return jsonify({
                    'status': 'success',
                    'message': 'Organisation created successfully',
                    'data': {
                         'orgId': organisation.orgId,
                         'name': name,
                         'description': description
                    }
               }), 201
     
          except Exception:
               return jsonify({
                    'status': 'Bad Request',
                    'message': 'Client error',
                    'statusCode': 400
               }), 400


@app.route('/api/organisations/<orgId>', methods=['GET'], strict_slashes=False)
@jwt_required()
def single_organisation(orgId):
     """ view that returns a single organisation 
     based on the orgId
     """

     if request.method == 'GET':
          organisation = Organisation.query.get(orgId)
          if not organisation:
               return jsonify({
                         'errors': [
                              {'field': 'orgId',
                              'message': 'invalid orgId'
                              }
                         ]     
                    }), 422

          return jsonify({
               'status': 'success',
               'message': 'single organisation',
               'data': {
                    'orgId': organisation.orgId,
                    'name': organisation.name,
                    'description': organisation.description
               }
          }), 200
     

@app.route('/api/organisations/<orgId>/', methods=['POST'], strict_slashes=False)
def add_user_organisation(orgId):
     """ view that handles adding a user to a particular organisation """

     try:
          userId = request.json.get('userId')
          if not userId:
               return jsonify({
                    'errors': [
                              {'field': 'userId',
                              'message': 'userId field cannot be blank'
                              }
                         ] 
               }), 422
          
          user = User.query.get(userId)

          organisation = Organisation.query.get(orgId)
          if not organisation:
               return jsonify({
                    'errors': [
                              {'field': 'orgId',
                              'message': 'invalid orgId'
                              }
                         ] 
               }), 422


          # adding the user to the organisation
          user.organisations.append(organisation)
          db.session.commit()

          return jsonify({
               'status': 'success',
               'message': 'User added to organisation successfully' 
          }), 200
     
     except Exception:
          return jsonify({
                    'errors': [
                              {'field': 'userId',
                              'message': 'invalid userId'
                              }
                         ] 
               }), 422 

        
if __name__ == '__main__':
    app.run(debug=True)
