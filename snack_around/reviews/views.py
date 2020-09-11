from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from .serializers import ReviewSerializer
from .permissions import ReviewsPermissions
from .models import Review


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

    def patch(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response({'review': 'review not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if review.author != user:
            return Response({'response': "You don't have permission to edit that."},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response({'review': 'review not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if review.author != user:
            return Response({'response': "You don't have permission to delete that."},
                            status=status.HTTP_401_UNAUTHORIZED)

        operation = review.delete()
        if operation:
            return Response()
        else:
            return Response({'response': "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = PageNumberPagination
