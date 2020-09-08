from rest_framework import serializers
from .models import Account, RestaurantInfo


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = ['address', 'phone_num']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    restaurant_info = RestaurantInfoSerializer(required=False)

    class Meta:
        model = Account
        fields = ['email', 'password', 'password2', 'username', 'restaurant_info', 'is_restaurant']
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
            restaurant_info = self.validated_data.pop('restaurant_info')
            info = RestaurantInfo.objects.create(restaurant=account, **restaurant_info)
            info.save()
        return account
