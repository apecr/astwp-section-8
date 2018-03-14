from tests.base_test import BaseTest
from models.user import UserModel
import json


class TestUser(BaseTest):

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertEqual(json.loads(response.data)['message'], 'The user has been created')

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                self.assertEqual(response.status_code, 201)
                auth_response = client.post('/auth',
                                            data=json.dumps({
                                                'username': 'test',
                                                'password': '1234'
                                            }),
                                            headers={
                                                'Content-Type': 'application/json'
                                            })

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                self.assertEqual(response.status_code, 201)
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(json.loads(response.data)['message'], 'A user with that username already exists')
