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
    user_name = db.Column(db.String(19), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    billing_address = db.Column(db.String(280))
    postal_code = db.Column(db.String(6))
    balance = db.Column(db.Integer)

    def __repr__(self):
        """
        Returns the class representation in string format.
        """
        return '<User %r>' % self.user_name
