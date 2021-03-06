from rest_framework import serializers
from PIL import Image
from django.contrib.auth import get_user_model
from .models import Account, RestaurantInfo, RestaurantImage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 3


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = ['address', 'phone_num']


class UserSerializer(serializers.ModelSerializer):
    info = RestaurantInfoSerializer(required=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'is_restaurant', 'is_customer', 'info']


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = '__all__'

    def validate(self, data):
        im = Image.open(data['image'])
        width, height = im.size
        aspect_ratio = width/height
        if aspect_ratio > 1.75 or aspect_ratio < 0.66:
            raise serializers.ValidationError({'image': 'wrong aspect ratio'})

        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    info = RestaurantInfoSerializer(required=False)

    class Meta:
        model = Account
        fields = ['id', 'email', 'password', 'password2', 'username', 'is_restaurant', 'is_customer', 'info']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'passwords must match'})
        return data

    def save(self, **kwargs):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            is_restaurant=self.validated_data['is_restaurant'],
            is_customer=not self.validated_data['is_restaurant'],
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        if account.is_restaurant:
            info = self.validated_data.pop('info')
            restaurant_info = RestaurantInfo.objects.create(restaurant=account, **info)
            restaurant_info.save()
        return account
