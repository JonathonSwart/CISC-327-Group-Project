"""
Module that structures different users Review data/tabel
"""

from .model_handler import db


class Reviews(db.Model):
    """
    The structure of how all these attributes will be added 
    inside of the sqlite database. All the attributes are below, 
    the unique ones and not nullables are specified
    """

    id = db.Column(db.Integer, primary_key=True)
    listing_id=db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.Boolean, unique=True, nullable=False)
    image_url  = db.Column(db.String(200), unique=True, nullable=False)
    review_date = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, unique=True, nullable=False)
    verified_guest = db.Column(db.Boolean, unique=True, default=False)
    review_title = db.Column(db.String(100), unique=True)
    

    #picture = db.Column(db.)

    def __repr__(self):
        """
        Returns the class representation in string format.
        """
        return '<Us er %r>' % self.username
  