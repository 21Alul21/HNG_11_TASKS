"""
module containing the database models for the
api project
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_organisation = db.Table('user_organisation',
    db.Column('user_id', db.String, db.ForeignKey('user.userId'), primary_key=True),
    db.Column('organisation_id', db.String, db.ForeignKey('organisation.orgId'), primary_key=True)
)

class User(db.Model):
    userId = db.Column(db.String, unique=True, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    organisations = db.relationship('Organisation', secondary=user_organisation, lazy='subquery',\
                                    backref=db.backref('users', lazy=True))
    def __repr__(self):
        return f'{self.userId} {self.firstName} {self.lastName}'

class Organisation(db.Model):
    orgId = db.Column(db.String, unique=True, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return f'{self.orgId} {self.name} {self.description}'

    
