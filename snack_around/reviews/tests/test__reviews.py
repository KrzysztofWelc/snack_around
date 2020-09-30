from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.serializers import RegistrationSerializer


class TestReviews(APITestCase):
    def setUp(self) -> None:
        data_restaurant = {
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
        user_serializer = RegistrationSerializer(data=data_restaurant)
        user_serializer.is_valid()
        self.user_restaurant = user_serializer.save()

        self.token_restaurant, _created = Token.objects.get_or_create(user=self.user_restaurant)

        data_client = {
            "email": "client@mail.com",
            "username": "client",
            "password": "1234",
            "password2": "1234",
            "is_restaurant": False
        }
        user_serializer = RegistrationSerializer(data=data_client)
        user_serializer.is_valid()
        self.user_client = user_serializer.save()

        self.token_client, _created = Token.objects.get_or_create(user=self.user_client)

    def test_add_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_client.key)

        data = {
            "score": 4,
            "text": "very cool xDD",
            "restaurant_id": self.user_restaurant.pk
        }

        res = self.client.post(
            '/api/reviews/',
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_client.key)

        data = {
            "score": 4,
            "text": "very cool xDD",
            "restaurant_id": self.user_restaurant.pk
        }

        res = self.client.post(
            '/api/reviews/',
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_get = self.client.get('/api/reviews/{}/'.format(res.data['id']))

        self.assertEqual(res_get.data['id'], res.data['id'])

    def test_edit_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_client.key)

        data = {
            "score": 4,
            "text": "very cool xDD",
            "restaurant_id": self.user_restaurant.pk
        }

        res = self.client.post(
            '/api/reviews/',
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_edit = self.client.patch(
            '/api/reviews/{}/'.format(res.data['id']),
            data={'score': 5}
        )

        self.assertEqual(res_edit.status_code, status.HTTP_200_OK)

        res_get = self.client.get('/api/reviews/{}/'.format(res.data['id']))
        self.assertEqual(res_get.data['score'], 5)

    def test_delete_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_client.key)

        data = {
            "score": 4,
            "text": "very cool xDD",
            "restaurant_id": self.user_restaurant.pk
        }

        res = self.client.post(
            '/api/reviews/',
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_delete = self.client.delete('/api/reviews/{}/'.format(res.data['id']))

        self.assertEqual(res_delete.status_code, status.HTTP_200_OK)

        res_get = self.client.get('/api/reviews/{}/'.format(res.data['id']))
        self.assertEqual(res_get.status_code, status.HTTP_404_NOT_FOUND)
