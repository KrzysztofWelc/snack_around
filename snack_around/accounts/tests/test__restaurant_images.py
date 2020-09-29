import io
from random import randint

from PIL import Image

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from ..serializers import RegistrationSerializer


class TestRestaurantImages(APITestCase):
    def setUp(self) -> None:
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
        user_serializer = RegistrationSerializer(data=data)
        user_serializer.is_valid()
        self.user = user_serializer.save()

        self.token, _created = Token.objects.get_or_create(user=self.user)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test{}.png'.format(randint(0, 100000))
        file.seek(0)
        return file

    def test_upload_single_image(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'images': [self.generate_photo_file()]
        }
        res = self.client.post(
            '/api/account/image',
            data,
            format='multipart'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res.data), 1)

    def test_upload_multiple_images(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'images': [self.generate_photo_file() for _ in range(3)]
        }
        res = self.client.post(
            '/api/account/image',
            data,
            format='multipart'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res.data), 3)

    def test_get_users_images(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'images': [self.generate_photo_file() for _ in range(3)]
        }
        res_add = self.client.post(
            '/api/account/image',
            data,
            format='multipart'
        )

        self.assertEqual(res_add.status_code, status.HTTP_201_CREATED)
        images_count = len(res_add.data)

        res_get = self.client.get(
            '/api/account/user_images/{}/'.format(self.user.pk)
        )
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_get.data), images_count)

    def test_delete_image(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'images': self.generate_photo_file()
        }
        res_add = self.client.post(
            '/api/account/image',
            data,
            format='multipart'
        )

        self.assertEqual(res_add.status_code, status.HTTP_201_CREATED)

        res_get = self.client.get(
            '/api/account/user_images/{}/'.format(self.user.pk)
        )
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)

        res_del = self.client.delete('/api/account/image/{}/'.format(res_get.data[0]['id']))
        self.assertEqual(res_del.status_code, status.HTTP_200_OK)

        res_confirm = self.client.get(
            '/api/account/user_images/{}/'.format(self.user.pk)
        )
        self.assertEqual(res_confirm.status_code, status.HTTP_200_OK)
        contains_deleted = res_get.data[0]['id'] in [obj['id'] for obj in res_confirm.data]
        self.assertFalse(contains_deleted)