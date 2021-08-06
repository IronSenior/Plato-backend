import unittest
import pytest
import uuid
from uuid import UUID
from ..brand_id import BrandId


@pytest.mark.unit
class TestBrandId(unittest.TestCase):

    def test_constructor(self):
        uniqueId = uuid.uuid4()
        brandId = BrandId(uniqueId)
        self.assertEqual(brandId.value, uniqueId)

    def test_from_string_constructor(self):
        uniqueId = str(uuid.uuid4())
        brandId = BrandId.fromString(uniqueId)
        self.assertEqual(brandId.value, UUID(uniqueId))

    def test_string_id(self):
        with self.assertRaises(TypeError):
            BrandId("24")

    def test_non_integer_usermail(self):
        with self.assertRaises(TypeError):
            BrandId(23.4)
