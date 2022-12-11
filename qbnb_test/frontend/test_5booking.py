from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User


class FrontEndRegisterPage(BaseCase):
    def test_booking_r1(self, *_):
        """
        Test if a user can book a listing
        """

        # Login a user
        self.open(base_url + "/login")
        # self.type("#username-input", "Jonathon S")
        # self.type("#email-input", "20js154@queensu.ca")
        # self.type("#password-input", "abc123DEF@")
        # self.click("#login-btn")

        self.type("#email-input", "19js154@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")

        balance = self.get_element("//*[@id='body']/div[2]/div[2]/div[1]/h4")
        balance = int(balance.text)

        self.click("#view-booking-btn")
        # prices = self.find_elements("#body > div:nth-child(2) > div:nth-child(2) > div > form:nth-child(3) > div.display-bookings > div:nth-child(3) > h6")

        listings = self.find_elements("#body > div:nth-child(2) > div:nth-child(2) > div > form:nth-child(3)")

        for listing in listings:
            price = self.find_element("#body > div:nth-child(2) > div:nth-child(2) > div > form:nth-child(3) > div.display-bookings > div:nth-child(3) > h6")
            price = int(price.text)
            if balance > price:
                self.click("#text")