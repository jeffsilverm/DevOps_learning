#! /usr/bin/env python3
#
import pytest
from flask import Flask
import json

DATABASE_FILENAME = "address_list.json"
SERVER_ADDR = "localhost"
SERVER_PORT = 5000
API_VERSION = "v1"


@pytest.mark.usefixtures('client_class')
class TestGet(object):
    db: dict = {"jeff": "jeffsilverm@gmail.com",
                "jeffs": "jeffsilverman.924@gmail.com"}

    @pytest.fixture(scope="session")
    def __init__(self) -> None:
        """Initialize the email database to a known state.  If there is an
        existing database file, destroy it"""

        with open(DATABASE_FILENAME, "w") as f:
            json.dump(self.db, fp=f)
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    @pytest.mark.parametrize("name,email_address", [
        ("jeffs", db["jeffs"]),
        ("jeff", db["jeff"])
    ])
    def test_get(self, name: str, email_address: str, client_uut) -> None:
        """Verify that when username is given, email_address is returned"""
        print(
            f"The type of client_uut is {type(client_uut)} name={name} addr="
            f"{email_address}")
        result = client_uut.get(
            f"http://{SERVER_ADDR}:{SERVER_PORT}/{API_VERSION}/{name}/")
        print(
            f"The response object is type {type(result)} has attributes "
            f"{dir(result)}")
        print(
            f"The response status={result.status} status_code="
            f"{result.status_code}")

        assert 200 == result.status_code, \
            f"status code should be 200, actually is {result.status_code}"
        assert email_address in result.read, \
            f"User {name} address={email_address} not in " \
            f"result.read {result.read}"


if "__main__" == __name__:
    testGet = TestGet()
    # This is adapted from https://github.com/aaronjolson/flask-pytest
    # -example/blob/master/tests/test_routes.py
    client = testGet.client
    print(f"client is {type(client)} {dir(client)}")
    print(f"dir(testGet)={dir(client)}")
    for k in testGet.db.keys():
        testGet.test_get(k, testGet.db[k], client_uut=client)
