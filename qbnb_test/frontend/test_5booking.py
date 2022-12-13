from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User


class FrontEndRegisterPage(BaseCase):
    def test_booking_r1(self, *_):
        """
        Uses output partitioning to test if a user can and cannot book a 
        listing
        """

        # Login a user
        self.open(base_url + "/login")

        self.type("#email-input", "19js154@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")

        # Can book a listing
        balance = self.get_element("//*[@id='body']/div[2]/div[2]/div[1]/h4")
        balance = str(balance.text)
        balance = int(balance[-2:])

        self.click("#view-booking-btn")

        prices = self.find_elements("""//*[@id='body']/div[2]/div[2]/div
        /form[*]/div[1]/div[3]/h6""")

        for idx, price in enumerate(prices):
            price = int(price.text)
            if balance >= price:
                self.click('/html/body/div[2]/div[2]/div/form[' + str(idx + 1)
                           + ']/div[2]/input')
                break

        self.click("//*[@id='body']/div[2]/div[2]/div/div/form[1]/input[2]")
        self.assert_text('Hello')

        # Can not book a listing
        balance = self.get_element("//*[@id='body']/div[2]/div[2]/div[1]/h4")
        balance = str(balance.text)
        balance = int(balance[-2:])

        self.click("#view-booking-btn")

        prices = self.find_elements("""//*[@id='body']/div[2]/div[2]/div
        /form[*]/div[1]/div[3]/h6""")

        for idx, price in enumerate(prices):
            price = int(price.text)
            if balance < price:
                self.click('/html/body/div[2]/div[2]/div/form[' + str(idx + 1)
                           + ']/div[2]/input')
                break

        self.click("//*[@id='body']/div[2]/div[2]/div/div/form[1]/input[2]")
        self.assert_text('Reserve This Listing Today')
