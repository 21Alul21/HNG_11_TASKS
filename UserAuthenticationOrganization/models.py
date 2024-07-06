"""
module containing the database models for the
api project
"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_organization = db.Table('user_organization',
    db.Column('user_id', db.String, db.ForeignKey('user.userId'), primary_key=True),
    db.Column('organization_id', db.String, db.ForeignKey('organization.orgId'), primary_key=True)
)

class User(db.Model):
    userId = db.Column(db.String, unique=True, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    organizations = db.relationship('Organization', secondary=user_organization, lazy='subquery',\
                                    backref=db.backref('users', lazy=True))

class Organization(db.Model):
    orgId = db.Column(db.String, unique=True, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
