"""
Module that declares the structure for a Transaction data model/table.
"""

from .model_handler import db


class PaymentInfo(db.Model):
    """Structures how the Users payment information entries will be
    stored in the database."""

    id = db.Column(db.Integer, primary_key=True)
    cardholder = db.Column(db.String(60), nullable=False)
    card_number = db.Column(db.Integer, unique=True, nullable=False)
    expiry_date = db.Column(db.Integer, nullable=False)
    CVV = db.Column(db.Integer, unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0.00)

    def __repr__(self):
        """Returns the class representation in string format."""
        return '<PaymentInfo %r>' % self.id


class RecieptInfo(db.Model):
    """Structures how the reciept information enteries will be
    stored in the database."""

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(60), nullable=False)
    listing_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        """Returns the class representation in string format."""
        return '<RecieptInfo %r>' % self.id
