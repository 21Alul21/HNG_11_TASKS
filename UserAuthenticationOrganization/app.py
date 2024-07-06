from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, User, Organization
import bcrypt
from auth_blueprint import JWT, auth
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb'
app.config['JWT_SECRETE_KEY'] = 'SFEFEFEVEVEVEVEV'

app.register_blueprint(auth)

db.init_app(app)
JWT.init_app(app)
     
@app.route('api/users/<id>', methods=['GET'], strict_slashes=None)
@jwt_required
def user_record(id):
      
      """ view that returns the user's record in organizations
        they belong to or created 
      """






              

        




        

     


        

         
         
        
if __name__ == '__main__':
    app.run(debug=True)
