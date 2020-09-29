import json
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_valid_client_registration(self):
        data = {
            "email": "client1@mail.com",
            "username": "client1",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": False
        }
        response = self.client.post('/api/account/register', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('token'))
        self.assertEqual(type(response.data.get('id')), int)
        self.assertEqual(response.data.get('username'), data['username'])
        self.assertEqual(response.data.get('email'), data['email'])
        self.assertEqual(response.data.get('info'), None)
        self.assertFalse(response.data.get('is_restaurant'))
        self.assertTrue(response.data.get('is_customer'))

    def test_invalid_email_client_registration(self):
        data = {
            "email": "client1@mail",
            "username": "client1",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": False
        }
        response = self.client.post('/api/account/register', data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_passwords_client_registration(self):
        data = {
            "email": "client1@mail.com",
            "username": "client1",
            "password": "1234",
            "password2": "12347",
            "is_restaurant": False
        }
        response = self.client.post('/api/account/register', data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_restaurant_registration(self):
        data = {
            "email": "restaurant1@mail.com",
            "username": "restaurant1",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": True,
            "info": {
                "address": "Hello st. 1",
                "phone_num": "999888777"
            }
        }
        response = self.client.post('/api/account/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('token'))
        self.assertEqual(type(response.data.get('id')), int)
        self.assertEqual(response.data.get('username'), data['username'])
        self.assertEqual(response.data.get('email'), data['email'])
        self.assertTrue(response.data.get('is_restaurant'))
        self.assertFalse(response.data.get('is_customer'))
        self.assertEqual(response.data['info'].get('address'), 'Hello st. 1')
        self.assertEqual(response.data['info'].get('phone_num'), '999888777')
