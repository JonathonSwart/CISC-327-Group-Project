from email import message
from flask import render_template, request, session, redirect
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from .models.User import User
from .backend_functions import create_listing, update_listing, register, update_profile, login

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
            id = session['logged_in']
            try:
                user = User.query.filter_by(id=id).one_or_none()
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


@app.route('/login', methods=['POST', 'GET'])
def login_get():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = login(email, password)
        if user:
            session['logged_in'] = user.id
            return render_template('login.html', message='Logged In!')
        else:
            return render_template('login.html', message='Incorrect email or password provided.')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_post():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        register_user = register(username, email, password)
        if register_user == True:
            return render_template('login.html', message='Login with your new account.')
        else:
            return render_template('register.html', message='One or more inputs have been entered incorrectly. Please try again.')
    return render_template('register.html')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/create-listing', methods=['POST', 'GET'])
def create_listing():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        nightly_cost = request.form['nightly-cost']
        valid_listing = create_listing(title, description, nightly_cost)
        if valid_listing is True:
            return render_template('home.html', message="Successful Listing Creation")
        else:
            return render_template('create_listing.html', message='Listing Creation Failed')