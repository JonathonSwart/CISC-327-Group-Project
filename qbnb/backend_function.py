"""file to run all the back end functions on for now"""

from __init__ import app 
from __init__ import db
from models.User import User
from models.Reviews import Reviews
import re
from models.Listing import Listing
from models.Transactions import RecieptInfo
from flask_sqlalchemy import SQLAlchemy
from models.Transactions import PaymentInfo
from models.model_handler import db

app.app_context().push()

def register(user_name, email, password):
    '''Register a new user'''
    # Check if any mandatory inputs are empty
    if((user_name == "") or (email == "") or (password == "")):
        return False
    # Check if the email is registered
    email_exist = User.query.filter_by(email=email).all()
    if(len(email_exist) > 0):
        return False
    else:
        # Check if the email matches the correct email regex.
        email_regex = r"""^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"""
        if (not (re.fullmatch(email_regex, email))):
            return False
    
register("Hi", "Hi", "hi")