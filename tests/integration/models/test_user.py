from tests.base_test import BaseTest
from models.user import UserModel


class TestUser(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')
            self.assertIsNone(UserModel.find_by_username(user.username))
            self.assertIsNone(UserModel.find_by_id(1))
            user.save_to_db()
            self.assertEqual(UserModel.find_by_username(user.username), user)
            self.assertEqual(UserModel.find_by_id(user.id), user)