from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if not data['restaurant'].is_restaurant:
            raise ValidationError({'restaurant': 'review\'s subject must me a restaurant'})

        return data
