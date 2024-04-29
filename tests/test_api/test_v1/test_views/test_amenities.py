import unittest
import json
from unittest.mock import patch, MagicMock
from api.v1 import app


class TestAmenityViews(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_get_all_amenities(self):
        with patch('models.storage.all') as mock_all:
            mock_all.return_value = {'1': MagicMock(to_dict=lambda: {'id': '1', 'name': 'Wifi'})}
            response = self.client.get('/api/v1/amenities')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['id'], '1')
            self.assertEqual(data[0]['name'], 'Wifi')

    def test_get_amenity(self):
        with patch('models.storage.get') as mock_get:
            mock_get.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Wifi'})
            response = self.client.get('/api/v1/amenities/1')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['id'], '1')
            self.assertEqual(data['name'], 'Wifi')

    def test_get_nonexistent_amenity(self):
        with patch('models.storage.get') as mock_get:
            mock_get.return_value = None
            response = self.client.get('/api/v1/amenities/123')
            self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        with patch('models.storage.get') as mock_get, \
             patch('models.storage.delete') as mock_delete, \
             patch('models.storage.save') as mock_save:
            mock_get.return_value = MagicMock()
            response = self.client.delete('/api/v1/amenities/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {})
            mock_delete.assert_called_once()
            mock_save.assert_called_once()

    def test_delete_nonexistent_amenity(self):
        with patch('models.storage.get') as mock_get:
            mock_get.return_value = None
            response = self.client.delete('/api/v1/amenities/123')
            self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        data = {'name': 'Pool'}
        with patch('models.storage.save') as mock_save, \
             patch('models.amenity.Amenity') as mock_amenity:
            mock_amenity.return_value = MagicMock(to_dict=lambda: {'id': '1', 'name': 'Pool'})
            response = self.client.post('/api/v1/amenities', json=data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(json.loads(response.data), {'id': '1', 'name': 'Pool'})
            mock_amenity.assert_called_once_with(**data)
            mock_save.assert_called_once()

    def test_create_amenity_missing_name(self):
        data = {}
        response = self.client.post('/api/v1/amenities', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing name', response.data)

    def test_create_amenity_invalid_json(self):
        response = self.client.post('/api/v1/amenities')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Not a JSON', response.data)

    def test_update_amenity(self):
        data = {'name': 'Gym'}
        with patch('models.storage.get') as mock_get, \
             patch('models.storage.save') as mock_save:
            amenity_mock = MagicMock()
            mock_get.return_value = amenity_mock
            response = self.client.put('/api/v1/amenities/1', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {'id': '1', 'name': 'Gym'})
            mock_get.assert_called_once_with('Amenity', '1')
            mock_save.assert_called_once()
            self.assertEqual(amenity_mock.name, 'Gym')

    def test_update_amenity_invalid_json(self):
        response = self.client.put('/api/v1/amenities/1')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Not a JSON', response.data)

    def test_update_amenity_nonexistent(self):
        data = {'name': 'Gym'}
        with patch('models.storage.get') as mock_get:
            mock_get.return_value = None
            response = self.client.put('/api/v1/amenities/1', json=data)
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
