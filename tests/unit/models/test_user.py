from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class TestUser(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Alberto', 'Alberto123')

        self.assertEqual(user.username, 'Alberto')
        self.assertEqual(user.password, 'Alberto123')
