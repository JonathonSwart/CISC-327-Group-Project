"""
Module that declares the structure for a Transaction data model/table.
"""

from .model_handler import db


class Booking(db.Model):
    """Structures how the Users payment information entries will be
    stored in the database."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, Unique=True, Nullable=False)
    listing_id = db.Column(db.Integer, Unique=True, Nullable=False)
    price = db.Column(db.Integer, Nullable=False)
    date = db.Column(db.DateTime, Nullable=False)

    def __repr__(self):
        """Returns the class representation in string format."""
        return '<PaymentInfo %r>' % self.id


