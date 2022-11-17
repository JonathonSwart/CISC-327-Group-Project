from seleniumbase import BaseCase
import time
from qbnb_test.conftest import base_url, pytest_sessionstart
from qbnb.backend_functions import register
from qbnb.models.User import User


class FrontEndRegisterPage(BaseCase):
    def test_env(self, *_):
        pytest_sessionstart()

    def test_r1_1_user_register(self, *_):
        """
        R1-1: Email cannot be empty. password cannot be empty.
        To test this requirement I will be doing black box output coverage
        testing. Since there is only one possible output for email and pass
        word being empty. In this test case the output should be that the
        user can not register.
        """

        # P1: Can not register output.
        self.open(base_url + '/register')
        self.type("#email-input", "")
        self.type("#password-input", "")
        time.sleep(2)
        self.click("#login-btn")

        # Check the output.
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

    def test_r1_3_user_register(self, *_):
        """
        R1-3: The email has to follow addr-spec defined in RFC 5322 (see 
        https://en.wikipedia.org/wiki/Email_address for a human-friendly exp
        lanation). You can use external libraries/imports.
        To test this user registeration, we will be using input partitioning
        testing. The email has to follow addr-spec defined in RFC 5322 gives
        provides us with only two partition test cases, where we are given
        an email who follows the RFC 5322 specification and an email who
        does not follow the RFC 5322 specifications. This does not check
        if an account is registered, only that the inputs provided do not
        break the program.
        """

        # P1 - Input does not follow the RFC 5532 specifications.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # P2 - Input does follow the RFC 5532 specifications.
        self.type("#email-input", "jeevan_start@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")
        self.assert_element("#message")
        self.assert_text(
            "Login with your new account.", "#message")

    def test_r1_4_user_register(self, *_):
        """
        R1-4: Password has to meet the required complexity: minimum 
        length 6, at least one upper case, at least one lower case, 
        and at least one special character. For this test, I will be 
        doing blackbox output coverage testing. There are only two 
        possible outputs given the requirement, where the first one 
        is given the correct password requirements an account is created. 
        Second where not following the requirements the user fails to 
        register.
        """

        # P1, given the wrong password requirements do not register.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_swag@gmail.com")
        self.type("#password-input", "4444")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")
        # Check the output.
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # P2, given the right password requirements do register.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_noswag@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")
        # Check the output.
        time.sleep(2)
        self.assert_element("#message")
        self.assert_text(
            "Login with your new account.", "#message")

    def test_r1_5_user_register(self, *_):
        """
        R1-5: User name has to be non-empty, alphanumeric-only, and 
        space allowed only if it is not as the prefix or suffix.
        For this test, I will be doing output testing. There are only two
        possible outputs given the requirement, where the first one is
        given the correct user_name requirements an account is created.
        Second where not following the requirements the user fails to
        register.
        """

        # P1, given the wrong username requirements do not register.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_foodie@gmail.com")
        self.type("#password-input", "4444")
        self.type("#username-input", " Jeevan ")
        time.sleep(2)
        self.click("#login-btn")
        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # P2, given the right username requirements do register.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_foodieswag@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "JeevanZ123")
        time.sleep(2)
        self.click("#login-btn")
        # Check the output.
        time.sleep(2)
        self.assert_element("#message")
        self.assert_text(
            "Login with your new account.", "#message")

    def test_r1_6_user_register(self, *_):
        """
        R1-6: User name has to be longer than 2 characters and less than 
        20 characters. For this test, we will be using the blackbox shotgun 
        testing method to check various lengths of usernames inputs and how 
        it is handled by the program. This will check whether the program 
        fails or can handle different situations. Since it is blackbox shot
        gun testing it will not be exhaustive and I will do it for 5 
        test cases.
        """

        # T1, a username less than 2 characters is provided.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "J")
        time.sleep(2)
        self.click("#login-btn")
        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # T2, a username greater than 20 characters is provided.
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeeeeeeeeeeeeeeeeeeen")
        time.sleep(2)
        self.click("#login-btn")
        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # T3, a username greater than 30 characters is provided.
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", """Jeeeeeeeeeeeeeeeeeeeee
        eeeeeeeeeen""")
        time.sleep(2)
        self.click("#login-btn")
        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # T4, a username greater than 40 characters is provided.
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", """EEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
        EEEEEEEEEEEEEEEEEEEEEEEEEEEEEE""")
        time.sleep(2)
        self.click("#login-btn")
        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")

        # T5, a username between 2 and 20 characters is provided.
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")
        # Verifying output
        self.assert_element("#message")
        self.assert_text(
            "Login with your new account.", "#message")

    def test_r1_7_user_register(self, *_):
        """
        R1-7: If the email has been used, the operation failed.
        To test this requirement I will be doing black box output coverage
        testing. Since emails need to be unique when registering, we will
        test with an already used email to get the output of this situation
        which is the user can not register. 
        """

        # A user trying to register with an already registered email.
        self.open(base_url + '/register')
        self.type("#email-input", "jeevan_louie@gmail.com")
        self.type("#password-input", "abc123DEF@")
        self.type("#username-input", "Jeevan123")
        time.sleep(2)
        self.click("#login-btn")

        # Verifiying output
        self.assert_element("#message")
        self.assert_text("One or more inputs have been entered incorrectly." +
                         " Please try again.", "#message")
