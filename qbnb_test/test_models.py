import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from qbnb_test.conftest import pytest_sessionfinish, pytest_sessionstart  # noqa
from qbnb.backend_functions import (create_listing, login, register,  # noqa
                                    update_profile, update_listing,  # noqa
                                    create_booking)  # noqa
from datetime import datetime  # noqa


"""
The reason we put no noqa is to get around an issue relating to vscode and
import issues.
"""


def test_env_start():
    '''
    Clearing the test enviroment. (Need this for pytest)
    '''

    pytest_sessionstart()


def test_r1_1_user_register():
    '''
    Testing R1-1 & 1 part of R1-5: If any of the provided inputs are empty, 
                                   the operation has failed.
    '''

    assert register('User1', 'test_user@gmail.com', 'abc123DEF@') is True
    assert register('', '', '') is False
    assert register('User1', 'test_user@gmail.com', '') is False


def test_r1_3_user_register():
    '''
    Testing R1-3: The email has to follow RFC 5322 specficitions.
    '''

    assert register('User2', 'test_user2@gmail.com', 'abc123DEF@') is True
    assert register('User2', 'test_user2', 'abc123DEF@') is False
    assert register('User2', 'test_user2@gmail', 'abc123DEF@') is False
    assert register('User2', '@gmail', 'abc123DEF@') is False


def test_r1_4_user_register():
    '''
    Testing R1-4: Checking if the passed password is at minimum length 6, at 
    least one upper case, at least one lower case, and at least one special 
    character.
    '''

    assert register('User3', 'test_user3@gmail.com', 'abc123DEF@') is True
    assert register('User3', 'test_user3@gmail.com', 'abc123DEF') is False
    assert register('User3', 'test_user3@gmail.com', 'a@') is False
    assert register('User3', 'test_user3@gmail.com', 'aAbccc') is False


def test_r1_5and6_user_register():
    '''
    Testing R1-5: Checking if the user_name is nonempty, alphanumeric-only,
    and space allowed only if it is not as the prefix or suffix.
    Testing R1-6: User name has to be longer than 2 characters and less 
    than 20 characters.
    '''

    assert register('User4', 'test_user4@gmail.com', 'abc123DEF@') is True
    assert register(' User2 ', 'test_user4@gmail.com', 'abc123DEF@') is False
    assert register('Jeevan Narewal', 'test_user4@gmail.com',
                    'abc123DEF@') is False
    assert register('JN', 'test_user4@gmail.com', 'abc123DEF@') is False


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed. Testing
    with the already added users from before.
    '''

    assert register('User5', 'test_user@gmail.com', 'abc123DEF@') is False
    assert register('User5', 'test_user2@gmail.com', 'abc123DEF@') is False
    assert register('User5', 'test_user3@gmail.com', 'abc123DEF@') is False
    assert register('User5', 'test_user5@gmail.com', 'abc123DEF@') is True


def test_r2_1_user_login():
    '''
    Testing R2-1: Can a user login, using an entry we created with the
    registration tests.
    '''

    user = login('test_user@gmail.com', 'abc123DEF@')
    assert user is not None
    assert user.user_name == 'User1'

    user = login('test_user@gmail.com', 'abc123DEF')
    assert user is None


def test_r4_1_create_listing():
    '''
    Testing R4-1 and R4-2. Title cannot have spaces as prefix or suffix
    and should be alhpanumeric and no longer than 80 characters
    '''
    # exclamation makes it not alphanumeric
    assert create_listing(
        "House title!", "this is the house description", 1000, 1) is False
    # title > 80 characters
    assert create_listing("House title is super long\
       longer than 80 characters\
       long so this should be false too!",
                          "this is the house description", 1000, 1) is False
    # title has spaces as prefix
    assert create_listing(
        " House title ", "this is the house description", 1000, 1) is False
    assert create_listing(
        "House title", "this is the house description", 1000, 1) is True


def test_r4_2_create_listing():
    '''
    Testing R4-3 and R4-4. description must be between 20 - 2000 
    characters long and longer than title description
    '''
    # too short descrption
    assert create_listing(
        "House title!", "description", 1000, 2) is False
    # really long description
    assert create_listing("House title is super long longer than\
       80 characters \long so this should be false too!",
                          "this is the house descriptionnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                      nnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnn\
                                      nnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnn\
                                      nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnn\
                              ", 1000, 2) is False
    # title is longer than description
    assert create_listing(
        "House title that is really long but valid still",
        "this is the house description", 1000, 2) is False
    # normal description
    assert create_listing(
        "House title2", "this is the house description", 1000, 2) is True


def test_r4_3_create_listing():
    """ 
    this function will check r4-5: if 
    the price range is between 10 - 10,000 dollars
    """
    # too small price
    assert create_listing(
        "House title3", "this is the house description", 5, 3) is False
    # too large price
    assert create_listing(
        "House title3", "this is the house description", 200000, 3) is False
    # within range price
    assert create_listing(
        "House title3", "this is the house description", 5000, 3) is True


def test_r4_4_create_listing():
    """ 
    This function will check r4-6 to 
    see if the date is within the required range 
    """
    # too early of date
    assert create_listing(
        "House title4", "this is the house description", 12, 4,
        datetime(2005, 1, 1)) is False
    # too late of date
    assert create_listing(
        "House title4", "this is the house description",
        2000, 4, datetime(2030, 1, 1)) is False
    # within correct date range
    assert create_listing(
        "House title4", "this is the house description", 5000, 4,
        datetime(2023, 1, 1)) is True


def test_r4_5_create_listing():
    """
     this function will check r4-7 and r4-8: the owner 
     must have valid username and account
    and each posting on the database must have a unique title
    """
    # Checking is user has valid account made and valid email
    assert create_listing(
        # no onwer_id 16 so should be false
        "House title5", "this is the house description", 1000, 160) is False
    # Owner_id 1 exists but title already used so should be false
    assert create_listing(
        "House title3", "this is the house description", 200, 1) is False
    # valid owner_id, email, and unique title name
    assert create_listing(
        "House title5", "this is the house description", 5000, 1) is True


def test_r3_1_update_profile():
    """
    Testing R3-1: A user is only able to update his/her user name, 
    user email, billing address, and postal code.
    """

    assert update_profile(1, None, None, None, None) is True
    assert update_profile(1, "Jonathon Swart", "19js154@queensu.ca",
                          None, None) is True
    assert update_profile(2, None, None, "100 ontario st", None) is True
    assert update_profile(3, None, None, None, "K7L1H6") is True
    assert update_profile(None, "Ash", None, None, None) is False


def test_r3_2and3_update_profile():
    """
    Test R3-2 and R3-3: postal code should be non-empty, 
    alphanumeric-only, and no special characters such as !. Postal code
    has to be a valid Canadian postal code.
    """

    assert update_profile(1, None, None, None, "K7L2T4") is True
    assert update_profile(2, None, None, None, "KKKKKK") is False
    assert update_profile(3, None, None, None, "K7L3N9L2H") is False


def test_r3_4_update_profile():
    """
    Test R3_4: User name should be non-empty, alphanumeric-only, and 
    no special characters such as !.
    """

    assert update_profile(1, "Ash K", None, None, None) is True
    assert update_profile(2, "Jonathon is the best!", None, None, None)\
        is False
    assert update_profile(4, "", None, None, None) is True
    assert update_profile(5, "jonathon@swart", None, None, None) is False


def test_r5_1_update_listing():
    """
    Test R5-1 & R5-3: One can update all attributes of the listing,
    except owner_id and last_modified_date. last_modified_date 
    should be updated when the update operation is successful.
    """
    assert update_listing(1, "New house title", "This is the new \
    house description", 1001) is True
    assert update_listing(2, "New house title", None, None) is True
    assert update_listing(
        3, None, "This is the new house Description", None) is True
    assert update_listing(4, None, None, 5000) is True


def test_r5_2_update_listing():
    """
    Test R5-2 & R5-3: Price can be only increased but cannot be decreased.
    last_modified_date should be updated when the update operation is 
    successful.
    """
    assert update_listing(4, None, None, 4000) is False
    assert update_listing(4, None, None, 6000) is True


def test_r6_1_create_booking():
    """
    Test R6-R1: A user can book a listing.
    """
    # First create a new listing we can test with.
    create_listing("Booking Sys Test", "Testing the Booking System",
                   10, 2)

    booking_date = datetime(2022, 11, 23)
    assert create_booking(1, 6, booking_date) is True
    assert create_booking(None, 6, booking_date) is False


def test_r6_2_create_booking():
    """
    Test R6-R2: A user cannot book their own listing.
    """
    booking_date = datetime(2022, 11, 24)
    assert create_booking(2, 6, booking_date) is False
    assert create_booking(1, 1, booking_date) is False


def test_r6_3_create_booking():
    '''
    Test R6-R3: A user cannot book a listing that costs
    more than their balance.
    '''
    # First create a new listing we can test with.
    create_listing("Booking Sys Test2", "Testing the Booking System",
                   10000, 2)
    create_listing("Booking Sys Test3", "Testing the Booking System",
                   30, 2)
    booking_date = datetime(2022, 11, 25)
    assert create_booking(1, 7, booking_date) is False
    assert create_booking(1, 8, booking_date) is True


def test_r6_4_create_booking():
    '''
    A user cannot book an already booked listing on a specific day.
    '''
    # Create a new listing we can work with
    create_listing("Booking Sys Test4", "Testing the Booking System",
                   30, 2)
    booking_date = datetime(2023, 1, 1)
    assert create_booking(1, 9, booking_date) is True
    assert create_booking(3, 9, booking_date) is False
    assert create_booking(1, 9, booking_date) is False


def test_env_end():
    '''
    Clearing the test enviroment. (Need this for pytest)
    '''

    pytest_sessionfinish()


if __name__ == '__main__':
    test_env_start()
    """
    Testing user registration requirements, skipping ones that don't involve
    user inputs.
    """
    test_r1_1_user_register()
    test_r1_3_user_register()
    test_r1_4_user_register()
    test_r1_5and6_user_register()
    test_r1_7_user_register()
    """
    Testing user login requirements, skipping ones that don't involve
    user inputs.
    """
    test_r2_1_user_login()
    test_r4_1_create_listing()
    test_r4_2_create_listing()
    test_r4_3_create_listing()
    test_r4_4_create_listing()
    test_r4_5_create_listing()
    """
    Testing update user profile requirements.
    """
    test_r3_1_update_profile()
    test_r3_2and3_update_profile()
    test_r3_4_update_profile()
    """
    Testing requirements outlined for update_listing()
    R5-4: update_listing uses the exact same code as
    create_listing(), as a result, those requirements
    are previously tested above in create_listing().
    """
    test_r5_1_update_listing()
    test_r5_2_update_listing()
    """
    Testing create booking requirements.
    """
    test_r6_1_create_booking()
    test_r6_2_create_booking()
    test_r6_3_create_booking()
    test_r6_4_create_booking()
    test_env_end()
