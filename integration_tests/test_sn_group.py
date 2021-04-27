import unittest
import pytest
import faker
import uuid
import json
from ..src.socialNetworkGroup.domain.repository.social_network_groups import SocialNetworkGroups
from ..src.socialNetworkGroup.domain.model.social_network_group_id import SocialNetworkGroupId
from ..src.socialNetworkGroup.domain.model.social_network_group import SocialNetworkGroup
from ..main import app, snGroupProvider

fake = faker.Faker()


@pytest.mark.integration
class TestSocialNetworkGroupIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.socialNetworkGroups: SocialNetworkGroups = snGroupProvider.SOCIAL_NETWORK_GROUPS()
        self.app = app.test_client()
        self.user_id = uuid.uuid4()
        self.access_headers = self.create_and_login_user()

    def create_and_login_user(self):
        email = fake.company_email()
        password = fake.password()
        self.app.post("/user/create/", json={
            "user": {
                "userid": str(self.user_id),
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

    def test_sn_group_creation(self):
        group_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/sn/group/create/", headers=self.access_headers, json={
            "snGroup": {
                "id": str(group_id),
                "userid": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        testing_group = self.socialNetworkGroups.getById(SocialNetworkGroupId.fromString(str(group_id)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(testing_group) == SocialNetworkGroup)
        self.assertEqual(testing_group.name, name)
        self.assertEqual(testing_group.image, image)

    def test_sn_group_with_other_user(self):
        group_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/sn/group/create/", headers=self.access_headers, json={
            "snGroup": {
                "id": str(group_id),
                "userid": str(uuid.uuid4()),
                "name": name,
                "image": image
            }
        })
        self.assertEqual(response.status_code, 401)

    def test_sn_group_without_login(self):
        group_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        response = self.app.post("/sn/group/create/", json={
            "snGroup": {
                "id": str(group_id),
                "userid": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        self.assertEqual(response.status_code, 401)

    def test_get_sn_group_by_user(self):
        group_id = uuid.uuid4()
        name = fake.company()
        image = fake.image_url()
        self.app.post("/sn/group/create/", headers=self.access_headers, json={
            "snGroup": {
                "id": str(group_id),
                "userid": str(self.user_id),
                "name": name,
                "image": image
            }
        })
        response = self.app.get(f"/sn/group/user/{self.user_id}/", headers=self.access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertTrue(str(group_id) in data.keys())

    def test_get_sn_group_by_user_with_other_user(self):
        response = self.app.get(f"/sn/group/user/{str(uuid.uuid4())}/", headers=self.access_headers)
        self.assertEqual(response.status_code, 401)

    def test_get_sn_group_by_user_without_login(self):
        response = self.app.get(f"/sn/group/user/{self.user_id}/")
        self.assertEqual(response.status_code, 401)
