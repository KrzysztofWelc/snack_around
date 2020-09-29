import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class LoginTestCase(APITestCase):

    def test_valid_login(self):
        reg_data = {
            "email": "client1@mail.com",
            "username": "client1",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": False
        }
        self.client.post('/api/account/register', reg_data)

        data = {
            "username": "client1@mail.com",
            "password": "1234"
        }
        response = self.client.post('/api/account/login', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.assertEqual(type(response.data['id']), int)
        self.assertEqual(response.data['email'], 'client1@mail.com')
        self.assertEqual(response.data['username'], 'client1')

    def test_invalid_login(self):
        reg_data = {
            "email": "client1@mail.com",
            "username": "client1",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": False
        }
        self.client.post('/api/account/register', reg_data)

        data = {
            "username": "client1@mail.com",
            "password": "12345"
        }
        response = self.client.post('/api/account/login', data)

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('token'))
