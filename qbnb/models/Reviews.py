"""
Module that structures different users Review data/tabel
"""

from time import timezone
from .model_handler import db
from datetime import datetime


class Reviews(db.Model):
    """
    The structure of how all these attributes will be added 
    inside of the sqlite database. All the attributes are below, 
    the unique ones and not nullables are specified
    """

    # entinties to have in our Review class
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    listing_id = db.Column(db.Integer, unique=True, nullable=False)
    review_text = db.Column(db.String(500), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """
        Returns the class representation in string format.
        """
        return f"Reviews('{self.id}', User id: '{self.user_id},\
        listing id '{self.listing_id}, reveiw_text '{self.review_text} \
        date '{self.date}')"
