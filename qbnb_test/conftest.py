import os
import sys
import pytest
import time
import threading
from werkzeug.serving import make_server
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from qbnb.models.model_handler import db  # noqa
from qbnb import app  # noqa
from qbnb.__main__ import FLASK_PORT  # noqa


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
    print("End of session.")


base_url = 'http://127.0.0.1:{}'.format(FLASK_PORT)


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # import necessary routes
        from qbnb import controllers
        self.srv = make_server('127.0.0.1', FLASK_PORT, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('running')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


@pytest.fixture(scope="session", autouse=True)
def server():
    # create a live server for testing
    # with a temporary file as database
    server = ServerThread()
    server.start()
    time.sleep(5)
    yield
    server.shutdown()
    time.sleep(2)
