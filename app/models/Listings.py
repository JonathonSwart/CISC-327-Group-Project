"""
Module that declares the structure for a Listing data model/table.
"""

from .model_handler import db

class Listing(db.Model):
    """The structure of how each Listing entry will be stored inside of 
    the sqlite database. It specifies which attributes are unique, what
    data goes into each field and any other notable properties.
    """
    id = db.Column(db.Integer, primary_key=True)
    listing_title = db.Coloumn(db.String(), nullable=False)
    username = db.Coloumn(db.String(), unique=True, nullable=False)
    username_notes = db.Coloumn(db.String(), unique=False)
    bedroom_count = db.Column(db.Integer, nullable=False)
    bed_count = db.Column(db.Integer, nullable=False)
    bath_count = db.Column(db.Integer, nullable=False)
    star_rating = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.json, nullable=False)  # Must figure out how to add list of strings to database
    country = db.Coloumn(db.String(), nullable=False)
    province_or_state = db.Coloumn(db.String(), nullable=False)
    city = db.Coloumn(db.String(), nullable=False)
    street = db.Coloumn(db.String(), nullable=False)
    postal_code = db.Coloumn(db.String(), nullable=False)
    gallery = db.Coloumn(db.json(), nullable=False)  # Must figure out how to add list of pics to database
    listing_notes = db.Coloumn(db.String(), nullable=False)
    availability = db.Column(db.json, nullable=False)  # Must figure out how to add calendar to database
    nightly_cost = db.Column(db.Integer, primary_key=True)
    amenities = db.Coloumn(db.String(), nullable=False)  # Must figure out how to add list of strings to database

    
    def __repr__(self):
        """Returns the class representation in string format."""
        return '<Listing: %r>' % self.listing_title