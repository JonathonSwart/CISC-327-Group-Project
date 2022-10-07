"""
The main file we will be using to manage the application and the 
database.
"""

from flask import Flask
from .models.model_handler import db
from .models.User import User
from .models.Reviews import Reviews
from .models.Listing import Listing
from .models.Booking import Booking


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
