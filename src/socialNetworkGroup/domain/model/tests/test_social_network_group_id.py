import unittest
import pytest
import uuid
from uuid import UUID
from ..social_network_group_id import SocialNetworkGroupId


@pytest.mark.unit
class TestSocialNetworkGroupId(unittest.TestCase):

    def test_constructor(self):
        uniqueId = uuid.uuid4()
        socialNetworkGroupId = SocialNetworkGroupId(uniqueId)
        self.assertEqual(socialNetworkGroupId.value, uniqueId)

    def test_from_string_constructor(self):
        uniqueId = str(uuid.uuid4())
        socialNetworkGroupId = SocialNetworkGroupId.fromString(uniqueId)
        self.assertEqual(socialNetworkGroupId.value, UUID(uniqueId))

    def test_string_id(self):
        with self.assertRaises(TypeError):
            SocialNetworkGroupId("24")

    def test_non_integer_usermail(self):
        with self.assertRaises(TypeError):
            SocialNetworkGroupId(23.4)
