from __init__ import db
from models.User import User
from models.Booking import Booking
from models.Listing import Listing
from models.Reviews import Reviews
from flask_sqlalchemy import SQLAlchemy
import re

# Register functions
def register(user_name, email, password):
    '''Register a new user'''
    # Check if any mandatory inputs are empty
    if((user_name == "") or (email == "") or (password == "")):
        return False
    # Check if the email is unique
    email_exist = User.query.filter_by(email=email).all()
    if(len(email_exist) > 0):
        return False
    else:
        pass

    user = User(user_name=user_name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

