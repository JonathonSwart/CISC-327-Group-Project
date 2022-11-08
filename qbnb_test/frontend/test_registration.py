from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User


class FrontEndRegisterPage(BaseCase):
    def test_register(self, *_):
        self.open(base_url)
