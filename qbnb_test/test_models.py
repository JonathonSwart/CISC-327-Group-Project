import __init__
from qbnb.backend_functions import login, register
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
    pytest_sessionfinish()
