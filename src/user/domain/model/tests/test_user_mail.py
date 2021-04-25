import unittest
import pytest
from ..user_mail import UserMail
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestUserMail(unittest.TestCase):

    def test_constructor(self):
        expectedValue = fake.company_email()
        usermail = UserMail(expectedValue)
        self.assertEqual(usermail.value, expectedValue)

    def test_from_string_constructor(self):
        expectedValue = fake.company_email()
        usermail = UserMail.fromString(expectedValue)
        self.assertEqual(usermail.value, expectedValue)

    def test_empty_mail(self):
        with self.assertRaises(UserMail.BadFormedEmail):
            UserMail("")

    def test_bad_usermail(self):
        with self.assertRaises(UserMail.BadFormedEmail):
            UserMail("John Cenna")
