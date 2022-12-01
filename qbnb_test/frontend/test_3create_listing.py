from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User
import string
import random


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class FrontEndRegisterPage(BaseCase):
    def test_home_page(self, *_):
        """
        This function using seleniumbase testing to 
        check if all the buttons on the home page work and if the proper 
        feilds are dislpaying.
        There is not much black box testing to check for this, as there is
         only minimal buttons to be clicked, but we can do input
         testing by clicking all buttons, and seeing  a result
         output.
         """

        # open web page
        self.open(base_url)

        # home page will redirect to log in so we test if we on log in page
        self.assert_title('Log In')
        # extra tests to see we are in the right URL.
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/login')
        self.assert_true("login" in get_started_url)

        # log in to get into home page
        # type in user name and password
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # Click submit button
        self.click('#login-btn')

        # check we are in home page
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/')

        # our input testing begins here
        # test what route each input brings us to
        self.click('#create-listing-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(
            get_started_url, base_url + '/create_listing')
        # click logout button
        self.click('#go-home-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/')

        # test show listing button
        self.click('#show-listing-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/listing')
        self.click('#home-btn')
        # go back home
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/?')

        # test update user porifle button
        self.click('#update-profile-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(
            get_started_url, base_url + '/update_profile')
        # go back home
        self.click('#update-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/')
        # test logout function
        self.click('#logout-btn')
        get_started_url = self.get_current_url()
        self.assert_equal(get_started_url, base_url + '/login')
        # end test
        self.assert_true("login" in get_started_url)

    def test_R4_1create_listing(self, *_):
        """
        This function is to test if the title does not have spaces 
        as prefix and suffix and is alphanumeric only. 
        We will do output testing
        Since we can only expect a result of fail message or success message 
        as our outputs. First we will test to see if we get fail message.
        """

        # open home page and log in with test account
        self.open(base_url)

        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(listing_url, base_url + '/create_listing')
        # now we can test the input feilds for create listing
        # we should see a account failed to be made message
        # as we pass in a title with special characters and space prefix
        self.type('#title-input', ' New title!')
        self.type('#description-input',
                  'this is a valid new house description')
        self.type('#cost-input', 1000)
        self.click('#create-ls-btn')
        self.assert_element("#message")
        # Output testing to see if output desired is acheived
        self.assert_text(
            "FAILED: Try again with different inputs", "#message")

        # now we test second output possibility which is
        # listing has been made

        self.type('#title-input', 'House title Success111')
        self.type('#description-input',
                  'this is a valid new house description yayy lets goo!!!')
        self.type('#cost-input', 1000)
        self.click('#create-ls-btn')
        self.assert_element("#message")
        self.assert_text('SUCCESS: Listing Created', '#message')
        # End of output test

    def test_R4_2create_listing(self, *_):
        """
        we will use input paritoin testing as a black box method
        to see if we get a success or failed output message, 
        based on whether the user enters a title that is longer 
        or shorter than 80 characters.
        We have 2 input: >80 characters and <80 characters
        """
        # open home page and log in with test account
        self.open(base_url)

        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(listing_url, base_url + '/create_listing')
        # add a title that is longer than 80 characters
        self.type('#title-input', ' New title that is very long \
        and even longer on this line and so long that it is\
            longer than 80 characters of length so it should\
                make the website fail')
        self.type('#description-input',
                  'this is a valid new house description')
        self.type('#cost-input', 1000)
        # submit above test input cases
        self.click('#create-ls-btn')
        self.assert_element("#message")
        # Output testing to see if output desired is acheived
        self.assert_text(
            "FAILED: Try again with different inputs", "#message")
        # if above test passed, we have our first test case T1
        # Now for test case T2 with a valid input
        self.type('#title-input', 'Appropriate Passing Title')
        self.type('#description-input',
                  'this is a valid new house description')
        self.type('#cost-input', 1000)
        # submit above test input cases
        self.click('#create-ls-btn')
        self.assert_element("#message")
        self.assert_text('SUCCESS: Listing Created', '#message')

    def test_R4_3create_listing(self, *_):
        """
        input partition + shotgun test:
        test case for requiremnet 3 of create listing. 
        Characters can be arbitrary but must be between 20-2000
        characters. We will use input partition 
        Black box Shotgun testing todecide the length of a randomly
        generated description and test the output accordingly. Our black box
        input partitions to test are descritions < 20 chars,
        descriptions > 2000 chars, and descriptions in between 20-200 chars
         """
        # open the web page
        self.open(base_url)
        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(
            listing_url, base_url + '/create_listing')
        # generate description string that is outside sepcifaction length
        # shotgun testing requires random values ran multiple times
        # so we use for loop
        # shotgun input partition test for values < 20 chars
        for i in range(0, 5):
            rand_description = get_random_string(random.randint(1, 19))
            self.type('#title-input', 'test title3')
            self.type('#description-input',
                      rand_description)
            self.type('#cost-input', 1000)
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element("#message")
            self.assert_text(
                "FAILED: Try again with different inputs", "#message")
        # now we do same test but for string > 2000 characters.
        # test should provide fail message output
        # due to long length of test, we do only 10 iterations. But
        # this can be changed as required
        for i in range(0, 5):
            rand_description = get_random_string(random.randint(2000, 2100))
            self.type('#title-input', 'test title3')
            self.type('#description-input',
                      rand_description)
            self.type('#cost-input', 1000)
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element("#message")
            self.assert_text(
                "FAILED: Try again with different inputs", "#message")
        # now we test with valid range
        test_title = 0
        for i in range(0, 5):
            rand_description = get_random_string(random.randint(21, 40))
            # automate random generation titles so there are no dups
            test_title = get_random_string(random.randint(10, 15))
            self.type('#title-input', test_title)
            self.type('#description-input',
                      rand_description)
            self.type('#cost-input', 1000)
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element("#message")
            self.assert_text('SUCCESS: Listing Created', '#message')
        # End of black box input partion shotgun test

    def test_R4_4create_listing(self, *_):
        """
        for this requirment, we will test that the description
        has to be longer than the title. We will use input partition
        + shotgun testing. Our two partitions are inputs where 
        the description is longer than the title and inputs where the product
        is not longer than the title of the product
        """
        # open the web page
        self.open(base_url)
        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(
            listing_url, base_url + '/create_listing')
        # test random values where title is longer than descirption
        # test should pass here as we won't be able to make account with
        # title < descirption
        for i in range(0, 5):
            title_string = get_random_string(random.randint(30, 40))
            description_string = get_random_string(random.randint(10, 20))
            self.type('#title-input', title_string)
            self.type('#description-input',
                      description_string)
            self.type('#cost-input', 1000)
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element("#message")
            self.assert_text(
                "FAILED: Try again with different inputs", "#message")
        # now we try but title > description
        for i in range(0, 5):
            title_string = get_random_string(random.randint(10, 20))
            description_string = get_random_string(random.randint(30, 50))
            self.type('#title-input', title_string)
            self.type('#description-input',
                      description_string)
            self.type('#cost-input', 1000)
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element("#message")
            self.assert_text('SUCCESS: Listing Created', '#message')
        # End Test Case

    def test_R4_5create_listing(self, *_):
        """
        This requirment test checks that the price is between a range of 
        10-10,000. We will Use input parition shotgun testing again
        for this test case. We have 3 paritions to do shotgun testing
        on. <10, inbetween 10-10,000 and > 10,000
        """
        # open the web page
        self.open(base_url)
        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(
            listing_url, base_url + '/create_listing')
        # begin shotgun test
        # test should always fail since price < 10
        for i in range(0, 5):
            title_string = get_random_string(random.randint(10, 20))
            description_string = get_random_string(random.randint(30, 40))
            self.type('#title-input', title_string)
            self.type('#description-input',
                      description_string)
            self.type('#cost-input', random.randint(0, 9))
            # submit inputs
            self.click('#create-ls-btn')
            self.click('#body')
            # random shotgun test should not pass since it
            # is outside required length

        # new test, should always fail since price > 10,000
        for i in range(0, 5):
            title_string = get_random_string(random.randint(10, 20))
            description_string = get_random_string(random.randint(30, 40))
            self.type('#title-input', title_string)
            self.type('#description-input',
                      description_string)
            self.type('#cost-input', random.randint(10001, 20000))
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.click('#body')
        # test parition for valid range of prices
        for i in range(0, 5):
            title_string = get_random_string(random.randint(10, 20))
            description_string = get_random_string(random.randint(30, 40))
            self.type('#title-input', title_string)
            self.type('#description-input',
                      description_string)
            self.type('#cost-input', random.randint(11, 9999))
            # submit inputs
            self.click('#create-ls-btn')
            # random shotgun test should not pass since it
            # is outside required length
            self.assert_element('#message')
            self.assert_text('SUCCESS: Listing Created', '#message')
        # End Of Test Case
        # requiremnt R4-6 will not be done as this is done in the backend

    def test_R4_8create_listing(self, *_):
        """
        Testing R4-8 a user cannot create products
        that have the same title. We will do input test on this. 
        Our two paritions are dup titles and non dupes. 
        """
        # open the web page
        self.open(base_url)
        # check title of tab
        self.assert_title('Log In')
        # fill in all the feilds
        self.type("#email-input", "test_user2@gmail.com")
        self.type('#password-input', 'abc123DEF@')
        # click the submit button
        self.click('#login-btn')
        # go to the create listing page
        self.click('#create-listing-btn')
        # check to see we are on right page
        listing_url = self.get_current_url()
        self.assert_equal(
            listing_url, base_url + '/create_listing')
        for i in range(0, 5):
            title_string = get_random_string(random.randint(10, 15))
            for j in range(0, 5):
                self.type('#title-input', title_string)
                self.type('#description-input',
                          'dummy description that can be the same')
                self.type('#cost-input', random.randint(11, 9999))
                # submit inputs
                self.click('#create-ls-btn')
                # random shotgun test should not pass since it
                # is outside required length
                self.assert_element("#message")
                # test should succeed first time but after dupes will be used
                # and tests should fail
                if j == 0:
                    self.assert_text('SUCCESS: Listing Created', '#message')
                else:
                    self.assert_text(
                        "FAILED: Try again with different inputs", "#message")
