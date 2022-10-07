from asyncio.windows_events import NULL
from __init__ import db
from models.User import User
from datetime import datetime
from models.Booking import Booking
from models.Listing import Listing
from models.Reviews import Reviews
from flask_sqlalchemy import SQLAlchemy
import re


# listing functions
def create_listing(title, description,  nightly_cost, owner_id, date=datetime.now()):
    '''Create a listing with specific requirments '''
    # checking to see if title is valid length and all alphanumeric and doesn't have space
    # as suffix or prefix

    title_regex = re.compile("^[a-zA-Z0-9 ]*$")
    if len(title) == 0 or len(title) > 80 or (not (re.fullmatch(title_regex, title)))\
            or title[0] == " " or title[-1] == " ":
        return False
    # if the description if shorter than the title it's not valid
    # if length is less than 20 characters or longer than 2000, it's not valid
    if (len(description) < len(title)) or (len(description) < 20) or (len(description) > 2000):
        return False
    # nightly cost has to be in range 10 - 10000
    if (nightly_cost < 10) or (nightly_cost > 10000):
        return False

    # if listing was not last updated in valid times then return False
    if (not (date > datetime(2021, 1, 2)) and (date < datetime(2025, 1, 2))):
        return False

    # check to see if title exists already, if it does send error since
    # title can't have same name twice in database
    existed = Listing.query.filter_by(title=title).all()
    if len(existed) > 0:
        return False

    # checking to see if owner email is valid
    user_object = User.query.filter_by(id=owner_id).first()
    if (user_object.email == "") or (user_object.email == None):
        return False

    listing1 = Listing(title=title, description=description,
                       nightly_cost=nightly_cost, last_modified_date=date, owner_id=owner_id)
    # add it to the current database session
    db.session.add(listing1)
    # actually save the user object
    db.session.commit()

    # if function executed completely and owner info is valid return True
    # so we can know function executed
    return True


user = User(password="password", email="ash.taraghi@gmail.com",
            billing_address="1029 freeman trail", postal_code="L9T 5T3", balance=2, user_name="ash taraghi")
db.session.add(user)
# actually save the user object
db.session.commit()
print(create_listing("House listing 1",
      "This is a great house! Buy before somoene else does!",  1000, 1))
