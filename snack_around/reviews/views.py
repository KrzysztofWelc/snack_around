from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReviewSerializer
from .permissions import ReviewsPermissions
from .models import Review
import pprint


class ReviewView(APIView):
    permission_classes = [ReviewsPermissions, ]

    def post(self, request, *args, **kwargs):
        restaurant_id = request.data.pop('restaurant_id')

        data = {
            'author': request.user.id,
            'restaurant': restaurant_id,
            **request.data
        }
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
