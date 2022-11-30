from flask import render_template, request, session, redirect, url_for
from .models.Booking import Booking
from .models.Listing import Listing
from .models.Reviews import Reviews
from .models.User import User
from datetime import datetime
from .backend_functions import create_listing, update_listing, register, \
    update_profile, login, create_booking

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
    id = user.id
    bookings = Booking.query.filter_by(user_id=id).all()
    listings_id = []
    # remove time date from the booking array
    for i in range(0, len(bookings)):
        bookings[i].date = bookings[i].date.date()
    # go through each booking of the user, grabbing respective listing id
    # add all the respective listing id's into it's own list
    for i in range(len(bookings)):
        listings_id.append(bookings[i].listing_id)
    listings = []
    # now we have a 2d array
    for i in listings_id:
        listings.append(Listing.query.filter_by(id=i).all())
    # convert to 1d
    final_listing = []
    for i in listings:
        for j in i:
            final_listing.append(j)
    print(final_listing)

    return render_template('home.html', user=user,
                           bookings=bookings, final_listing=final_listing)


@app.route('/logout')
def logout():
    # When you logout you redirect to home which redirects
    # for you to log in first
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/bookings', methods=['GET', 'POST'])
def booking():
    '''
    Will redirect to a page where all the viewable bookings can be seen. 
    Cannot view this page unless user is logged in.
    To avoid being able to book your own booking, 
    only other user's booking will be dispalys, however, 
    backend code exists to protect this too.
    '''
    if 'logged_in' in session:
        pass
    else:
        return redirect('/login')
    id = session['logged_in']
    listings = Listing.query.all()
    # remove any of the user's own listings from the
    # list and pass onto the front end
    for i in listings:
        if (i.owner_id == id):
            listings.remove(i)
    return render_template('bookings.html', listings=listings)


@app.route('/reserving', methods=['GET', 'POST'])
def reserve():
    '''
    This is the route for booking a listing with the avaible dates.
    '''
    if 'logged_in' in session:
        pass
    else:
        return redirect('/login')
    if request.method == "POST":
        message = ""
        listing_id = request.form['data']
        id = session['logged_in']
        return render_template('reserve.html', listing_id=listing_id,
                               id=id, message=message)

    return render_template('reserve.html')


@app.route('/reserved', methods=['POST', 'GET'])
def book():
    if 'logged_in' in session:
        pass
    else:
        return redirect('/login')
    if request.method == "POST":
        listing_id = request.form['listing_id']
        id = request.form['id']
        date = request.form['datetime']
        date = date.split('-')
        for i in range(0, len(date)):
            date[i] = date[i].lstrip('0')
        final_date = datetime(
            int(date[0]), int(date[1]), int(date[2]))
        booked = create_booking(id, listing_id, final_date)
        if booked:
            return redirect('/')
        else:
            return render_template(
                'reserve.html',
                message="There was a problem making this booking")

    return render_template('reserve.html', message="")


@app.route('/update_profile', methods=['POST', 'GET'])
def update_profiles():
    """
    Will update the database with the new email, username, address, and
    postal code inputted by the user. If the user successfully updates
    their profile, they will be redirected to the home page.
    """
    if 'logged_in' in session:
        pass
    else:
        return redirect('/login')

    if request.method == "POST":
        username = request.form['username']
        new_email = request.form['new_email']
        address = request.form['address']
        postal_code = request.form['postal_code']
        if 'logged_in' in session:
            user_id = session['logged_in']
        update_pf = update_profile(user_id, username, new_email, address,
                                   postal_code)
        if update_pf is True:
            return redirect('/')
        else:
            return render_template('update_profile.html',
                                   message="""Something 
                                    went wrong. Invalid input.""")
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
            new_nightly_cost = new_nightly_cost
            if new_nightly_cost == "":
                new_nightly_cost = None
            elif new_nightly_cost is not None:
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
def create_listings():
    if 'logged_in' in session:
        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']
            nightly_cost = request.form['nightly-cost']
            user_id = session['logged_in']
            valid_listing = create_listing(title, description,
                                           int(nightly_cost), int(user_id))
            if valid_listing is True:
                return render_template('create_listing.html',
                                       message="SUCCESS: Listing Created")
            else:
                return render_template('create_listing.html',
                                       message='FAILED:\
                                       Try again with different inputs')
        return render_template('create_listing.html')
    else:
        return redirect('/login')
