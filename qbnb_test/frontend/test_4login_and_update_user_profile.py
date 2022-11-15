from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User


class FrontEndRegisterPage(BaseCase):
    def test_r2_1_2_login(self, *_):
        """
        Uses black box output partition testing to test that a user
        can properly login to a registered account.
        """

        # Resister a user
        self.open(base_url + "/register")
        self.type("#username-input", "Jonathon S")
        self.type("#email-input", "20js154@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")

        self.type("#email-input", "test")
        self.type("#password-input", "test")
        self.click("#login-btn")
        self.assert_exact_text("Login", "h1")

        self.type("#email-input", "20js154@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")
        self.assert_text_visible("Hello", "h1")

    def test_r3_1_update_user_profile(self, *_):
        """
        Uses functionality coverage to test that a user is only able to
        update his/her user name, user email, billing address, and 
        postal code.
        """

        # Logging in user
        self.open(base_url + "/login")
        self.type("#email-input", "20js154@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")
        self.click('a:contains("Update Profile")')

        # Check that all inputs work
        self.type("#username-input", "Jonathon S")
        self.type("#email-input", "tesing123@queensu.ca")
        self.type("#address-input", "27 mack st")
        self.type("#postal_code-input", "K7L1N3")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

        # Check each input works independently
        # Check username
        self.click('a:contains("Update Profile")')
        self.type("#username-input", "Ash K")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

        # Check email
        self.click('a:contains("Update Profile")')
        self.type("#email-input", "js1234@queensu.ca")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

        # Check address
        self.click('a:contains("Update Profile")')
        self.type("#address-input", "100 nelson rd")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

        # Check postal code
        self.click('a:contains("Update Profile")')
        self.type("#postal_code-input", "K7L4T5")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

    def test_r3_2_3_4_update_user_profile(self, *_):
        """
        Uses input partitioning to test that a postal code should be 
        non-empty, alphanumeric-only, and no special characters such as !.
        As well a postal code has to be a valid Canadian postal code. User 
        name follows the requirements above.
        """

        # Logging in user
        self.open(base_url + "/login")
        self.type("#email-input", "js1234@queensu.ca")
        self.type("#password-input", "abc123DEF@")
        self.click("#login-btn")
        self.click('a:contains("Update Profile")')

        # Both user name and postal code are valid
        self.type("#username-input", "Jonathon S")
        self.type("#postal_code-input", "K7L1N3")
        self.click("#update-profile-btn")
        self.assert_text_visible("Hello", "h1")

        # User name is valid but postal is not valid
        self.click('a:contains("Update Profile")')
        self.type("#username-input", "Ash K")
        self.type("#postal_code-input", "K7L!@#")
        self.click("#update-profile-btn")
        self.assert_exact_text("Update Profile", "h1")

        # User name is not valid but postal code is valid
        self.type("#username-input", "Jonathon@@@Swart")
        self.type("#postal_code-input", "K7L1N3")
        self.click("#update-profile-btn")
        self.assert_exact_text("Update Profile", "h1")

        # User name is not valid and postal code is not valid
        self.type("#username-input", "Jonathon@@@Swart")
        self.type("#postal_code-input", "K7L!@#")
        self.click("#update-profile-btn")
        self.assert_exact_text("Update Profile", "h1")
