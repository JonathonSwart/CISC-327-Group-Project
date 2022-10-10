import os
from qbnb.models.model_handler import db


def pytest_sessionstart():
    '''
    Delete database file if existed. So testing can start fresh.
    '''

    print('Setting up environment..')
    db_file = 'qbnb/db.sqlite'
    if os.path.exists('qbnb/db.sqlite'):
        os.remove(db_file)
        db.create_all()
    elif os.path.exists('instance/db.sqlite'):
        os.remove('instance/db.sqlite')
        db.create_all()


def pytest_sessionfinish():
    '''
    Optional function called when testing is done.
    Do nothing for now
    '''
    print("Done Testing")
