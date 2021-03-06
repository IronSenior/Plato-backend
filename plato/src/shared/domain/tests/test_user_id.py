import unittest
import uuid
from uuid import UUID
from ..user_id import UserId


class TestUserId(unittest.TestCase):

    def test_constructor(self):
        uniqueId = uuid.uuid4()
        userId = UserId(uniqueId)
        self.assertEqual(userId.value, uniqueId)

    def test_from_string_constructor(self):
        uniqueId = str(uuid.uuid4())
        userId = UserId.fromString(uniqueId)
        self.assertEqual(userId.value, UUID(uniqueId))

    def test_string_id(self):
        with self.assertRaises(TypeError):
            UserId("24")

    def test_non_integer_usermail(self):
        with self.assertRaises(TypeError):
            UserId(23.4)
