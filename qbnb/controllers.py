from flask import render_template, request, session, redirect
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from .models.User import User
from .backend_functions import create_listing, update_listing, register, update_profile

from qbnb import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def home():
    return render_template('register.html')
