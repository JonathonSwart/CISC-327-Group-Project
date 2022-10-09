import __init__
from datetime import datetime
from qbnb.backend_functions import login, register, create_listing
from conftest import pytest_sessionstart, pytest_sessionfinish


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
    assert create_listing("House title is super long longer than 80 characters\
       long so this should be false too!",
                          "this is the house description", 1000, 1) is False
    # title has spaces as prefix
    assert create_listing(
        " House title ", "this is the house description", 1000, 1) is False
    assert create_listing(
        "House title", "this is the house description", 1000, 1) is True


def test_r4_2_create_listing():
    '''
    Testing R4-3 and R4-4. description must be between 20 - 2000 characters long and longer
    than title description
    '''
    # too short descrption
    assert create_listing(
        "House title!", "description", 1000, 2) is False
    # really long description
    assert create_listing("House title is super long longer than 80 characters\
       long so this should be false too!",
                          "this is the house descriptionnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                            nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                  nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                                nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\
                              ", 1000, 2) is False
    # title is longer than description
    assert create_listing(
        "House title that is really long but valid still", "this is the house description", 1000, 2) is False
    # normal description
    assert create_listing(
        "House title2", "this is the house description", 1000, 2) is True


def test_r4_3_create_listing():
    """ 
    this function will check r4-5: if the price range is between 1 - 10,000 dollars
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
    This function will check r4-6 to see if the date is within the required range 
    """
    # too early of date
    assert create_listing(
        "House title4", "this is the house description", 12, 4, datetime(2005, 1, 1)) is False
    # too late of date
    assert create_listing(
        "House title4", "this is the house description", 2000, 4, datetime(2030, 1, 1)) is False
    # within correct date range
    assert create_listing(
        "House title4", "this is the house description", 5000, 4, datetime(2023, 1, 1)) is True


def test_r4_5_create_listing():
    """
     this function will check r4-7 and r4-8: the owner must have valid username and account
    and each posting on the database must have a unique title
    """
    # Checking is user has valid account made and valid email
    print("this")
    assert create_listing(
        # no onwer_id 16 so should be false
        "House title5", "this is the house description", 1000, 160) is False
    # Owner_id 1 exists but title already used so should be false
    assert create_listing(
        "House title3", "this is the house description", 200, 1) is False
    # valid owner_id, email, and unique title name
    assert create_listing(
        "House title5", "this is the house description", 5000, 1) is True


if __name__ == '__main__':
    pytest_sessionstart()
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
    pytest_sessionfinish()
