import re
from flask_sqlalchemy import SQLAlchemy
from .__init__ import db
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from .models.User import User


# Register functions
def register(user_name, email, password):
    '''
    Registers a new user into the system.
        Parameters:
            user_name (string): The user's user name.
            email (string):     The user's email.
            password (string):  The user's password.
        Returns:
            True if the registeration goes through and the new user is created
            otherwise False. 
    '''
    # Check if any mandatory inputs are empty
    if ((user_name == "") or (email == "") or (password == "")):
        return False
    # Check if the email is unique & valid.
    email_exist = User.query.filter_by(email=email).all()
    if (len(email_exist) > 0):
        return False
    else:
        # Check if the email is valid with RFC 5322
        email_regex = re.compile(r"""([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0
                                      -9-]+(\.[A-Z|a-z]{2,})+""")
        if (not (re.fullmatch(email_regex, email))):
            return False
    # Check if the password is valid.
    password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$"
    if (not (re.fullmatch(password_regex, password))):
        return False
    # Check if user-name is valid.
    if ((len(user_name) < 20) and (len(user_name) > 2)):
        user_name_regex = re.compile(r"^[a-zA-Z0-9][ a-zA-Z0-9]*[a-zA-Z0-9]+")
        if (not (re.fullmatch(user_name_regex, user_name))):
            return False
    else:
        return False
    # Register the user in the data_base, with a free sign-up bonus of 100.
    user = User(user_name=user_name, email=email, password=password,
                balance=100)
    # Add the user to the database.
    db.session.add(user)
    # Save the user object.
    db.session.commit()
    return True


def login(email, password):
    '''
    Checks if the login information being provided by a user exists in our 
    database.
        Parameters:
            email (string):     The user's email.
            password (string):  The user's password.
        Returns:
            A user object if the login is successful otherwise None, if input
            fields are invalid None is returned too.
    '''
    # Check if any mandatory inputs are empty
    if ((email == "") or (password == "")):
        print("One or more inputs is empty.")
        return None
    # Check if the email is unique & valid.
    email_exist = User.query.filter_by(email=email).all()
    if (len(email_exist) < 1):
        return None
    else:
        # Check if the email is valid with RFC 5322
        email_regex = re.compile(r"""([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0
                                      -9-]+(\.[A-Z|a-z]{2,})+""")
        if (not (re.fullmatch(email_regex, email))):
            return None
    # Check if the password is valid.
    password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$"
    if (not (re.fullmatch(password_regex, password))):
        return None
    # Find the specified user in the database and return it.
    user_data = User.query.filter_by(email=email, password=password).all()
    if len(user_data) != 1:
        return None
    return user_data[0]
