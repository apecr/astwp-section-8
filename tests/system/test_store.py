from tests.base_test import BaseTest
from models.store import StoreModel
from models.item import ItemModel
import json


class TestSystemStore(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertEqual(json.loads(response.data), {'name': 'test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                response_delete = client.delete('/store/test')

                self.assertEqual(response_delete.status_code, 200)
                self.assertEqual(json.loads(response_delete.data)['message'], 'Store deleted')
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                response_get = client.get('/store/test')

                self.assertEqual(response_get.status_code, 200)
                self.assertEqual(json.loads(response_get.data),
                                 {'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response_get = client.get('/store/test')

                self.assertEqual(response_get.status_code, 404)
                self.assertEqual(json.loads(response_get.data)['message'], 'Store not found')

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')
                item = ItemModel('Car', 200.00, 1)
                store.save_to_db()
                item.save_to_db()

                response_get = client.get('/store/test')
                self.assertEqual(response_get.status_code, 200)
                self.assertEqual(json.loads(response_get.data),
                                 {'name': 'test',
                                  'items': [{
                                      'name': 'Car',
                                      'price': 200.00
                                  }]})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                store1 = StoreModel('Vehicles')
                store2 = StoreModel('Furniture')
                item11 = ItemModel('Car', 200.00, 1)
                item12 = ItemModel('Motorbike', 300.00, 1)
                item21 = ItemModel('Chair', 50.00, 2)
                item22 = ItemModel('Table', 80.00, 2)
                store1.save_to_db()
                store2.save_to_db()
                item11.save_to_db()
                item12.save_to_db()
                item21.save_to_db()
                item22.save_to_db()

                response_list = client.get('/stores')
                self.assertEqual(response_list.status_code, 200)
                self.assertEqual(json.loads(response_list.data)['stores'],
                                 [
                                     {
                                         'name': 'Vehicles',
                                         'items': [
                                             {
                                                 'name': 'Car',
                                                 'price': 200.00
                                             },
                                             {
                                                 'name': 'Motorbike',
                                                 'price': 300.00
                                             }
                                         ]
                                     },
                                     {
                                         'name': 'Furniture',
                                         'items': [
                                             {
                                                 'name': 'Chair',
                                                 'price': 50.00
                                             },
                                             {
                                                 'name': 'Table',
                                                 'price': 80.00
                                             }
                                         ]
                                     }
                                 ])

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Vehicles').save_to_db()

                response_list = client.get('/stores')
                self.assertEqual(response_list.status_code, 200)
                self.assertEqual(json.loads(response_list.data)['stores'],
                                 [{
                                     'name': 'Vehicles',
                                     'items': []
                                 }])
