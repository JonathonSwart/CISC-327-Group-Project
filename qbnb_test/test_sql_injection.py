import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from qbnb_test.conftest import pytest_sessionfinish, pytest_sessionstart  # noqa
from qbnb.backend_functions import (create_listing, register, create_booking)  # noqa
from datetime import datetime  # noqa


"""
The reason we put no noqa is to get around an issue relating to vscode and
import issues.
"""


def test_sql_injection_test():
    pytest_sessionstart()
    with open('qbnb_test/sql_injection.txt', 'r') as file:
        for payload in file:
            print("The current payload is : " + payload)
            # SQL injection testing with the register function.

            # Try to register with payload on the user_name field.
            try:
                register(payload, "jeevan_roblox@gmail.com", "abc123DEF@")
            except Exception as error:
                print("Exception Thrown for user_name payload: "
                      + str(error))
            # Try to register with payload on the email field.
            try:
                register("Jeevan", payload, "abc123DEF@")
            except Exception as error:
                print("Exception Thrown for email payload: " + str(error))
            # Try to register with payload on the password field.
            try:
                register("Jeevan", "jeevan_roblox@gmail.com", payload)
            except Exception as error:
                print("Exception Thrown for password payload:" + str(error))

            # SQL injection testing with the create_listing function.

            # Try to create a listing with payload on the title field.
            try:
                create_listing(
                    payload, "this is the house description", 5000, 1)
            except Exception as error:
                print("Exception Thrown for title payload: " + str(error))
            # Try to create a listing with payload on the description field.
            try:
                create_listing("SQL Inject Listing", payload, 5000, 1)
            except Exception as error:
                print("Exception Thrown for description payload: " +
                      str(error))
            # Try to create a listing with payload on the nightly_cost field.
            try:
                create_listing(
                    "SQL Inject Listing", "this is the house description",
                    payload, 1)
            except Exception as error:
                print("Exception Thrown for nightly cost payload: "
                      + str(error))
            # Try to create a listing with payload on the owner_id field.
            try:
                create_listing(
                    "SQL Inject Listing", "this is the house description",
                    5000, payload)
            except Exception as error:
                print("Exception Thrown for date_time payload: "
                      + str(error))

            # SQL injection testing with the create booking function.

            # Try to create a booking with payload on the user_id
            try:
                create_booking(payload, 1, datetime(2023, 1, 1))
            except Exception as error:
                print("Exception thrown for user_id payload: "
                      + str(error))
            # Try to create a booking with payload on the listing_id
            try:
                create_booking(1, payload, datetime(2023, 1, 1))
            except Exception as error:
                print("Exception thrown for listing_id payload: "
                      + str(error))
            # Try to create a booking with payload on the booking_date
            try:
                create_booking(1, 1, payload)
            except Exception as error:
                print("Exception thrown for user_id payload: "
                      + str(error))

    pytest_sessionfinish()
