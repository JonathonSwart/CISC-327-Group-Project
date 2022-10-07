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
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    nightly_cost = db.Column(db.Integer, primary_key=True, nullable=False)
    last_modified_date = db.Column(db.String(), nullable=False)

    def __repr__(self):
        """Returns the class representation in string format."""
        return '<Listing: %r>' % self.title
