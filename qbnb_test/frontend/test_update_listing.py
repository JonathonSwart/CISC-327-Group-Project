from seleniumbase import BaseCase
from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models.User import User
import time


class UpdateListingPage(BaseCase):
    def test_update_listing(self, *_):

        # Creating a listing to test with
        self.open(base_url + "/login")
        self.find_element("#email-input").send_keys("19js154@queensu.ca")
        self.find_element('#password-input').send_keys("abc123DEF@")
        self.find_element('#login-btn').click()
        self.find_element('/html/body/div[2]/div[2]/div/div/a[2]').click()
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()

        # OUTPUT PARTITION TESTING
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[3]').send_keys("9")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element('//*[@id="new-cost"]').send_keys('1200')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # FUNCTIONALITY TESTING; Testing the create listing requirements
        #  from sprint 2
        # R5-1,2,3,4
        # "Title must be alphanumeric Only"
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "upd@te house")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "updated house")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # "Title only allows space if it is not a prefix and/or suffix"
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                " update house")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "update house ")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")

        # Title of product is no longer than 80 characters
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit." +
            " Aenean commodo ligula eget")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "Updated house")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # Description has a mimimum length of 20 characters
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
                "min len 20")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
            "This description is over 20 characters")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # Description has a maximum length of 2000 characters
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]' +
            '/div[2]/div/form' +
            '/input[2]').send_keys(
            "Lorem ipsum dolor sit amet, " +
            "consectetuer adipiscing elit." +
            " Aenean commodo ligula eget dolor. " +
            "Aenean massa. Cum sociis natoque" +
            " penatibus et magnis dis parturient" +
            " montes, nascetur ridiculus mus." +
            " Donec quam felis, ultricies nec," +
            " pellentesque eu, pretium quis, " +
            "sem. Nulla consequat massa quis" +
            " enim. Donec pede justo, fringilla" +
            " vel, aliquet nec, vulputate" +
            " eget, arcu. In enim justo, rhoncus" +
            " ut, imperdiet a, venenatis" +
            " vitae, justo. Nullam dictum felis" +
            " eu pede mollis pretium. Integer" +
            " tincidunt. Cras dapibus. Vivamus" +
            " elementum semper nisi. Aenean" +
            " vulputate eleifend tellus. Aenean" +
            " leo ligula, porttitor eu, " +
            "consequat vitae, eleifend ac, enim." +
            " Aliquam lorem ante, dapibus" +
            " in, viverra quis, feugiat a, tellus." +
            " Phasellus viverra nulla ut " +
            " metus varius laoreet. Quisque rutrum." +
            " Aenean imperdiet. Etiam" +
            " ultricies nisi vel augue. Curabitur " +
            "ullamcorper ultricies nisi." +
            " Nam eget dui. Etiam rhoncus. Maecenas" +
            " tempus, tellus eget cond" +
            "imentum rhoncus, sem quam semper libero," +
            " sit amet adipiscing sem" +
            " neque sed ipsum. Nam quam nunc, blandit " +
            "vel, luctus pulvinar," +
            " hendrerit id, lorem. Maecenas nec odio" +
            " et ante tincidunt tempus." +
            " Donec vitae sapien ut libero venenatis" +
            " faucibus. Nullam quis ante." +
            " Etiam sit amet orci eget eros faucibus" +
            " tincidunt. Duis leo. Sed" +
            " fringilla mauris sit amet nibh. Donec " +
            "sodales sagittis magna. " +
            "Sed consequat, leo eget bibendum sodales," +
            " augue velit cursus nunc," +
            " quis gravida magna mi a libero. Fusce" +
            " vulputate eleifend sapien." +
            " Vestibulum purus quam, scelerisque ut" +
            ", mollis sed, nonummy id," +
            " metus. Nullam accumsan lorem in dui." +
            " Cras ultricies mi eu tur" +
            "pis hendrerit fringilla. Vestibulum ante" +
            " ipsum primis in faucib" +
            "us orci luctus et ultrices posuere " +
            "cubilia Curae; In ac dui quis" +
            " mi consectetuer lacinia. Nam pretium " +
            "turpis et arcu. Duis arcu" +
            " tortor, suscipit eget, imperdiet nec," +
            " imperdiet iaculis, ipsum" +
            ". Sed aliquam ultrices mauris. Integer" +
            " ante arcu, accumsan a, " +
            "consectetuer eget, posuere ut, mauris. " +
            "Praesent adipiscing. Pha" +
            "sellus ullamcorper ipsum rutrum nunc. Nunc" +
            " nonummy metus. Vestib" +
            "ulum volutpat pretium libero. Cras id dui." +
            " Aenean ut eros et nisl" +
            " sagittis vestibulum. Nullam nulla")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
            "This description is under 2000 characters")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # Description has to be longer than title
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys("short")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
            "This description is longer than the title")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        # Price has to be more than 10
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[3]').send_keys("5")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element('//*[@id="new-cost"]').send_keys('1201')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update

        # Price has to be less than 10000
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[3]').send_keys(
                "30000000")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element('//*[@id="new-cost"]').send_keys('1202')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update

        # Price cannot decrease, only increase
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[3]').send_keys('5')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 2
        self.find_element('//*[@id="new-cost"]').send_keys('1203')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update

        # SHOTGUN TESTING
        # Test 1
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        self.find_element('//*[@id="new-cost"]').send_keys('1204')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
        self.find_element(
            '/html/body/div[2]/div[2]/div/div[1]/div/form/h4/button').click()
        # Test 2
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys("fgs@ ")
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "this IS TEStin&")
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 3
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
                " jsnfjisndngjnj#) ")
        self.find_element('//*[@id="new-cost"]').send_keys('14')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 4
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
                " jsnfjisndngjnj#) ")
        self.find_element('//*[@id="new-cost"]').send_keys('12')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        # Failed to update
        self.assert_text("one or more inputs are incorrect")
        # Test 5; R5-
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[1]').send_keys(
                "Final updated house")
        self.find_element(
            '/html/body/div[2]/div[2]/div/form/input[2]').send_keys(
            "This is the final updated description")
        self.find_element('//*[@id="new-cost"]').send_keys('1205')
        self.find_element('/html/body/div[2]/div[2]/div/form/button').click()
        self.assert_text("Ash K Listing's:")  # Successful update
