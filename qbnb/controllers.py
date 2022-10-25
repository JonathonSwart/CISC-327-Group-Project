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
            return redirect('/')
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


@app.route('/', methods=['GET', 'POST'])
@authenticate
def home(user):
    return render_template('home.html', user=user)


@app.route('/logout')
def logout():
    # When you logout you redirect to home which redirects
    # for you to log in first
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/update-profile', methods=['POST', 'GET'])
def update_profiles():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        new_email = request.form['new_email']
        address = request.form['address']
        postal_code = request.form['postal_code']
        user = User.query.filter_by(email=email).first()
        user_id = user.id
        update_pf = update_profile(user_id, username, new_email, address, postal_code)
        if update_pf is True:
            return redirect(url_for("home"))
        else:
            return render_template('update_profile.html', message='Email verification failed. Please enter a valid email.')
    return render_template('update_profile.html')


@app.route('/listing', methods=['GET'])
def listing():
    if 'logged_in' in session:
        id = session['logged_in']
        user = User.query.filter_by(id=id).one_or_none()
        listings = Listing.query.filter_by(owner_id=id).all()
        return render_template('listing.html', user=user, listings=listings)
    else:
        return redirect('/login')


@app.route('/select_update_listing', methods=['GET', 'POST'])
def select_update_listing():
    if request.method == "POST":
        data = request.form['data']
        listing = Listing.query.filter_by(id=data).one_or_none()
        if listing:
            print(listing)
            return render_template('update_listing.html', listing=listing)
        else:
            return redirect('/')
    return render_template('update_listing.html', listing=listing)


@app.route('/update_listing', methods=['GET', 'POST'])
def updating_listing():
    if 'logged_in' in session:
        if request.method == "POST":
            data = request.form['data']
            listing = Listing.query.filter_by(id=data).one_or_none()
            new_title = request.form['new-title']
            new_description = request.form['new-description']
            new_nightly_cost = request.form['new-cost']
            new_nightly_cost = int(new_nightly_cost)
            updated = update_listing(
                data, new_title, new_description, new_nightly_cost)
            if updated:
                return redirect('/listing')
            else:
                return render_template(
                    'update_listing.html',
                    listing=listing,
                    message="one or more inputs are incorrect")
    else:
        return redirect('/')


@app.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    # luca this ones yours
    if 'logged_in' in session:
        return render_template('create_listing.html')
    else:
        return redirect('/login')
