"""
Module that declares the structure for a User data model/table.
"""

from .model_handler import db


class User(db.Model):
    """The structure of how each User entry will be stored inside of 
    the sqlite database. It specifies which attributes are unique, what
    data goes into each field and any other notable properties.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    street = db.Column(db.String(500), nullable=False)
    postal_code = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    is_host = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        """
        Returns the class representation in string format.
        """
        return '<User %r>' % self.username
