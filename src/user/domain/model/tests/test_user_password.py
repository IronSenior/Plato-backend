import unittest
from passlib.hash import sha256_crypt
from ..user_password import UserPassword


class TestPassword(unittest.TestCase):

    def test_constructor(self):
        password = UserPassword(sha256_crypt.hash("password"))
        self.assertTrue(sha256_crypt.verify("password", password.value))

    def test_from_string(self):
        password = UserPassword.fromString("password")
        self.assertTrue(sha256_crypt.verify("password", password.value))

    def test_if_can_verify(self):
        password = UserPassword.fromString("password")
        self.assertTrue(password.verify("password"))
        self.assertFalse(password.verify("notPassword"))