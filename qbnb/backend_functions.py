from .__init__ import db
from .models.User import User
from datetime import datetime
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from flask_sqlalchemy import SQLAlchemy
import re

# listing functions


def create_listing(title, description, nightly_cost,
                   owner_id, date=datetime.now()):
    '''
    Create a listing with specific requirments
    '''
    # checking to see if title is valid length and
    # all alphanumeric and doesn't have space
    # as suffix or prefix

    title_regex = re.compile("^[a-zA-Z0-9 ]*$")
    if len(title) == 0 or len(title) > 80 or \
        (not (re.fullmatch(title_regex, title)))\
            or title[0] == " " or title[-1] == " ":
        return False
    # if the description if shorter than the title it's not valid
    # if length is less than 20 characters or longer than 2000, it's not valid
    if (len(description) < len(title)) or \
            (len(description) < 20) or (len(description) > 2000):
        return False
    # nightly cost has to be in range 10 - 10000
    if (nightly_cost < 10) or (nightly_cost > 10000):
        return False

    # if listing was not last updated in valid times then return False
    if ((date < datetime(2021, 1, 2)) or ((date > datetime(2025, 1, 2)))):
        return False

    # check to see if title exists already, if it does send error since
    # title can't have same name twice in database
    existed = Listing.query.filter_by(title=title).all()
    if len(existed) > 0:
        return False

    # checking to see if owner email is valid
    user_object = User.query.filter_by(id=owner_id).first()
    # print(user_object.email)
    if user_object is None:
        return False
    elif user_object.email == "":
        return False

    listing1 = Listing(title=title, description=description,
                       nightly_cost=nightly_cost, owner_id=owner_id,
                       last_modified_date=date)
    # add it to the current database session
    db.session.add(listing1)

    db.session.commit()
    return True


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
        # The regex has to stay as 1 line so it exceeds the 79 character
        # count otherwise issues occur.
        email_regex = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")  # noqa
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

    # if function executed completely and owner info is valid return True
    # so we can know function executes


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


def update_profile(user_id, new_username, new_email, new_billing_address,
                   new_postal_code):
    """Updates a users profile to new changes
        Parameters:
            user_id (integer):              The user's user id.
            new_username (string):          The user's new user name.
            new_email (string):             The user's new email.
            new_billing_address (string):   The user's new billing address.
            new_postal_code (string):       The user's new postal code.
        Returns:
            True if updates to user's profile are committed successfully
            and false otherwise.
    """

    # Checks if user id was inputted
    if (user_id is None):
        return False

    user = User.query.get(user_id)  # Get user
    send_error = False

    # Update users username
    username_regex = re.compile(r"""^[a-zA-Z0-9][ a-zA-Z0-9]*[a-zA-Z0-9]+""")
    if (new_username is None or new_username == ""):
        pass
    else:
        # Checks if username is valid
        if (new_username != "" and (len(new_username) > 2 and
                                    len(new_username) < 20)):
            if (re.fullmatch(username_regex, new_username)):
                user.user_name = new_username
            else:
                send_error = True
        else:
            send_error = True

    # Update users email
    if (new_email is None or new_email == ""):
        pass
    else:
        email_regex = re.compile(r"""([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0
                                      -9-]+(\.[A-Z|a-z]{2,})+""")
        # Checks if email is valid
        if (new_email != "" and re.fullmatch(email_regex, new_email)):
            user.email = new_email

        else:
            send_error = True

    # Update users billing address
    if (new_billing_address is None or new_billing_address == ""):
        pass
    else:
        # Checks if billing address is valid
        address_regex = re.compile(r"^([0-9]+( [A-Za-z0-9]+)+)")
        if ((new_billing_address != "") and
                (re.fullmatch(address_regex, new_billing_address))):
            user.billing_address = new_billing_address
        else:
            send_error = True

    # Update users postal code
    postal_code_regex = re.compile(r"""^([A-Z][0-9][A-Z][0-9][A-Z][0-9])$""")
    if (new_postal_code is None or new_postal_code == ""):
        pass
    else:
        # Checks if postal code is valid
        if (new_postal_code != "" and len(new_postal_code) == 6):
            if (re.fullmatch(postal_code_regex, new_postal_code)):
                user.postal_code = new_postal_code
            else:
                send_error = True
        else:
            send_error = True

    # Commit changes
    db.session.commit()

    # Returns false so program knows function did not work
    if (send_error is True):
        return False
    else:
        return True


def update_listing(listing_id, new_title, new_description, new_nightly_cost):
    '''
    Update a listing with specific requirments
        Parameters:
            listing_id (string): The user's user name.
            new_title (string):     The user's email.
            new_description (string):  The user's password.
            new_nightly_cost (int):
        Returns:
            True if a listing is successfully updated, returns False if a 
            single field does not meet its standards
    '''
    # checking to see if title is valid length and
    # all alphanumeric and doesn't have space
    # as suffix or prefix

    listing = Listing.query.get(listing_id)
    bool_return = True

    if (new_title is None or new_title == ""):
        pass
    else:
        title_regex = re.compile("^[a-zA-Z0-9 ]*$")
        if len(new_title) == 0 or len(new_title) > 80 or \
            (not (re.fullmatch(title_regex, new_title))) \
                or new_title[0] == " " or new_title[-1] == " ":
            bool_return = False
        else:
            listing.title = new_title

    # if the description if shorter than the title it's not valid
    # if length is less than 20 characters or longer than 2000, it's not valid
    if (new_description is None or new_description == ""):
        pass
    else:
        if (len(new_description) < len(listing.title) or
                len(new_description) < 20 or len(new_description) > 2000):
            bool_return = False
        else:
            listing.description = new_description

    # nightly cost has to be in range 10 - 10000
    # new nightly cost must be greater than the previous nightly cost
    if (new_nightly_cost is None or new_nightly_cost == ""):
        pass
    else:
        if (10 > new_nightly_cost or new_nightly_cost > 10000 or
            new_nightly_cost
                < listing.nightly_cost):
            bool_return = False
        else:
            listing.nightly_cost = new_nightly_cost

    # if any of the fields are not safely updated, return False
    if (bool_return is False):
        return False
    else:
        listing.last_modified_date = datetime.now()
        db.session.commit()
    return True


def create_booking(user_id, listing_id, booking_date):
    '''
    Create a booking entry in the database based off the user chooing
    to create the booking.
    Parameters:
            user_id (int):              The id of the user booking the 
                                        listing.
            lisitng_id (int) :          The id of the listing having a 
                                        booking being created for it.
            booking_date (datetime) :   The date in which the user is 
                                        booking the listing.
        Returns:
            A user object if the login is successful otherwise None, if input
            fields are invalid None is returned too.
    '''
    # First check that the user_id does exist in the data base.
    user_object = User.query.filter_by(id=user_id).first()
    if user_object is None:
        print("User no exist.")
        return False
    # Next check that the listing does exist in the data base.
    listing_object = Listing.query.filter_by(id=listing_id).first()
    if listing_object is None:
        print("Lising no exist")
        return False
    # Make sure that the user is not booking their own listing.
    if (listing_object.owner_id == user_id):
        print("user owns listing")
        return False
    # Check whether the user can afford the listing.
    if (user_object.balance < listing_object.nightly_cost):
        print("user no afford")
        return False
    # Check whether bookings exists for the listing, make sure no booking
    # on the same date exists.
    listing_bookings = Booking.query.filter_by(listing_id=listing_id).all()
    if (len(listing_bookings) > 0):
        # Loop through all the bookings and check the date they were created.
        for booking in listing_bookings:
            if (booking.date == booking_date):
                print("Time found")
                return False
    new_booking = Booking(user_id=user_id, listing_id=listing_id,
                          price=listing_object.nightly_cost,
                          date=booking_date)
    user_object.balance -= listing_object.nightly_cost
    db.session.add(new_booking)
    db.session.commit()
    return True
