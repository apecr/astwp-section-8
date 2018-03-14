from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({
                                                'username': 'test',
                                                'password': '1234'
                                            }),
                                            headers={
                                                'Content-Type': 'application/json'
                                            })
                auth_token = json.loads(auth_response.data)['access_token']
                self.auth_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(401, resp.status_code)
                self.assertEqual('Could not authorize. Did you include a valid Authorization header?',
                                 json.loads(resp.data)['message'])

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp_get = client.get('/item/test', headers={'Authorization': self.auth_token})
                self.assertEqual(404, resp_get.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                ItemModel('Car', 20.00, 1).save_to_db()
                resp_get = client.get('/item/Car', headers={'Authorization': self.auth_token})
                self.assertEqual(200, resp_get.status_code)
                self.assertEqual({
                    'name': 'Car',
                    'price': 20.00
                }, json.loads(resp_get.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                ItemModel('Car', 20.00, 1).save_to_db()
                resp_delete = client.delete('/item/Car', headers={'Authorization': self.auth_token})
                self.assertEqual(200, resp_delete.status_code)
                self.assertIsNone(ItemModel.find_by_name('Car'))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                resp_create = client.post('/item/Car', data={'price': 20.00, 'store_id': 1},
                                          headers={'Authorization': self.auth_token})
                self.assertEqual(201, resp_create.status_code)
                self.assertEquals(ItemModel.find_by_name('Car').json(), json.loads(resp_create.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                ItemModel('Car', 20.00, 1).save_to_db()
                resp_create = client.post('/item/Car', data={'price': 20.00, 'store_id': 1},
                                          headers={'Authorization': self.auth_token})
                self.assertEqual(400, resp_create.status_code)
                self.assertEquals({'message': "An item with name 'Car' already exists."}, json.loads(resp_create.data))

    def test_put_item_new(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                resp_put_new = client.put('/item/Car', data={'price': 20.00, 'store_id': 1},
                                          headers={'Authorization': self.auth_token})
                self.assertEqual(200, resp_put_new.status_code)
                self.assertEquals(ItemModel.find_by_name('Car').json(), json.loads(resp_put_new.data))

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                ItemModel('Car', 20.00, 1).save_to_db()
                resp_put = client.put('/item/Car',
                                      data=json.dumps({'price': 30.00, 'store_id': 1}),
                                      headers={
                                          'Authorization': self.auth_token,
                                          'Content-Type': 'application/json'
                                      })
                self.assertEqual(200, resp_put.status_code)
                self.assertEquals(30.00, json.loads(resp_put.data)['price'])
                self.assertEquals(ItemModel.find_by_name('Car').json(), json.loads(resp_put.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()
                ItemModel('Car', 20.00, 1).save_to_db()
                ItemModel('Bike', 10.00, 1).save_to_db()
                resp_get = client.get('/items', headers={
                                          'Authorization': self.auth_token,
                                          'Content-Type': 'application/json'
                                      })
                self.assertEqual(200, resp_get.status_code)
                self.assertEqual(2, len(json.loads(resp_get.data)['items']))

