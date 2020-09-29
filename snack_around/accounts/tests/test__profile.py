from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from ..serializers import RegistrationSerializer


class TestProfiles(APITestCase):
    def create_user(self, index=1):
        data = {
            "email": "restaurant{}@mail.com".format(index),
            "username": "restaurant{}".format(index),
            "password": "1234",
            "password2": "1234",
            "is_restaurant": True,
            "info": {
                "address": "Hello st. {}".format(index),
                "phone_num": "999888777"
            }
        }
        user_serializer = RegistrationSerializer(data=data)
        user_serializer.is_valid()
        user = user_serializer.save()

        token, _created = Token.objects.get_or_create(user=user)
        return {
            'token': token,
            'user': user
        }

    def test_get_current_user(self):
        user_data = self.create_user()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_data['token'].key)
        res = self.client.get('/api/account/me')

        self.assertEqual(user_data['user'].email, res.data['email'])

    def test_get_single_restaurant(self):
        users = []
        for index in range(6):
            users.append(self.create_user(index))

        res = self.client.get(
            '/api/account/restaurant/{}/'.format(users[0]['user'].pk)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_restaurants_pagination(self):
        for i in range(30):
            self.create_user(i)

        res = self.client.get('/api/account/restaurants')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['next'])
        self.assertFalse(res.data['previous'])
