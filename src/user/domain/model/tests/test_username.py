
import unittest
import pytest
from ..username import Username
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestUserName(unittest.TestCase):

    def test_correct_constructor(self):
        expectedValue = fake.first_name()
        userName = Username(expectedValue)
        self.assertEqual(userName.value, expectedValue)

    def test_from_string_constructor(self):
        expectedValue = fake.first_name()
        userName = Username.fromString(expectedValue)
        self.assertEqual(userName.value, expectedValue)

    def test_bad_name(self):
        with self.assertRaises(Username.BadFormedUserName):
            Username("")

    def test_username_with_spaces(self):
        with self.assertRaises(Username.BadFormedUserName):
            Username("John Cenna")
