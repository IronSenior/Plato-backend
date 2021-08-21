import unittest
import faker
import uuid
import json
from ..src.brand.domain.repository.brands import Brands
from ..src.brand.domain.model.brand_id import BrandId
from ..src.brand.domain.model.brand import Brand
from ..main import create_app, brandProvider
fake = faker.Faker()


class TestBrandIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.brands: Brands = brandProvider.BRANDS()
        self.app = create_app(test_env=True).test_client()
        self.user_id = uuid.uuid4()
        self.access_headers = self.create_and_login_user()

    def create_and_login_user(self):
        email = fake.company_email()
        password = fake.password()
        self.app.post("/user/create/", json={
            "user": {
                "userId": str(self.user_id),
                "username": fake.first_name(),
                "usermail": email,
                "password": password
            }
        })
        login_response = self.app.post("/user/login/", json={
            "email": email,
            "password": password,
        })
        data = json.loads(login_response.data)
        headers = {
            'Authorization': 'Bearer {}'.format(data["access_token"])
        }
        return headers

    def test_brand_creation(self):
        brand_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/brand/create/", headers=self.access_headers, json={
            "brand": {
                "id": str(brand_id),
                "userId": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        testing_brand = self.brands.getById(BrandId.fromString(str(brand_id)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(testing_brand) == Brand)
        self.assertEqual(testing_brand.name, name)
        self.assertEqual(testing_brand.image, image)

    def test_brand_with_other_user(self):
        brand_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/brand/create/", headers=self.access_headers, json={
            "brand": {
                "id": str(brand_id),
                "userId": str(uuid.uuid4()),
                "name": name,
                "image": image
            }
        })
        self.assertEqual(response.status_code, 401)

    def test_brand_without_login(self):
        brand_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/brand/create/", json={
            "brand": {
                "id": str(brand_id),
                "userId": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        self.assertEqual(response.status_code, 401)

    def test_get_brand_by_user(self):
        brand_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        self.app.post("/brand/create/", headers=self.access_headers, json={
            "brand": {
                "id": str(brand_id),
                "userId": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        response = self.app.get(f"/brand/user/{self.user_id}/", headers=self.access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertTrue(str(brand_id) in data.keys())

    def test_get_brand_by_user_with_other_user(self):
        response = self.app.get(f"/brand/user/{str(uuid.uuid4())}/", headers=self.access_headers)
        self.assertEqual(response.status_code, 401)

    def test_get_brand_by_user_without_login(self):
        response = self.app.get(f"/brand/user/{self.user_id}/")
        self.assertEqual(response.status_code, 401)
