import unittest
import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4
from ..create_brand_handler import CreateBrandHandler
from ..create_brand_command import CreateBrandCommand
from ....domain.model.brand import Brand
from ....domain.model.brand_id import BrandId
from ....domain.model.brand_name import BrandName
from ....domain.model.brand_image import BrandImageUrl
from ....domain.exceptions.brand_id_aready_registered import BrandIdAlreadyRegistered
from .....user.domain.model.user_id import UserId
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestCreateBrandHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedBrandRepository = Mock()
        self.createBrandHandler = CreateBrandHandler(
            brands=self.mockedBrandRepository
        )
        return super(TestCreateBrandHandler, self).setUp()

    def test_create_a_new_brand(self):
        self.createBrandHandler.handle(
            CreateBrandCommand(
                id=str(uuid4()),
                userId=str(uuid4()),
                name=fake.first_name(),
                image=fake.image_url()
            )
        )
        self.mockedBrandRepository.save.assert_called_once()

    def test_dont_create_duplicate_brand_id(self):
        user = Brand.add(
            id=BrandId.fromString(str(uuid4())),
            userId=UserId.fromString(str(uuid4())),
            name=BrandName.fromString(fake.first_name()),
            image=BrandImageUrl.fromString(fake.image_url())
        )
        self.mockedBrandRepository.getById = MagicMock(return_value=user)
        self.assertRaises(BrandIdAlreadyRegistered,
                          self.createBrandHandler.handle, CreateBrandCommand(
                              id=str(uuid4()),
                              userId=str(uuid4()),
                              name=fake.first_name(),
                              image=fake.image_url()
                          ))
