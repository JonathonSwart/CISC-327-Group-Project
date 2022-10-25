from flask import render_template, request, session, redirect
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from .models.User import User
from .backend_functions import create_listing, update_listing, register, \
                                update_profile, login

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
    """
    Sets the session logged_in value to the fetched user from the provided
    email and password. When the user logs in it redirects them to the home
    page.
    """

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = login(email, password)
        if user:
            session['logged_in'] = user.id
            # Change this line so thath the user is sent to the home page
            # when they log in.
            return render_template('login.html', message='Logged In!')
        else:
            return render_template('login.html',
                                   message="""Incorrect email or 
                                   password provided.""")
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_post():
    """
    When a user registers an account, the provided username, email and 
    password are sent to the register function in the backend. Creating
    an account with the given information and then redirecting the user 
    to the login page.
    """

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        register_user = register(username, email, password)
        if register_user:
            return render_template('login.html',
                                   message='Login with your new account.')
        else:
            return render_template('register.html', message="""One or more 
            inputs have been entered incorrectly. Please try again.""")
    return render_template('register.html')
