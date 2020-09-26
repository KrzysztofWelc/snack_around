from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsCustomer, IsRestaurant
from .serializers import ProductSerializer
from .models import Product


class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'product': 'product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProductSerializer(instance=product).data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated, IsRestaurant])
    def post(self, request, *args, **kwargs):
        user = request.user
        data = {**request.data, 'restaurant': user.pk}

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated, IsRestaurant])
    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'product': 'product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if product.restaurant.pk != user.pk:
            return Response({'response': 'You cannot edit that'}, status=status.HTTP_401_UNAUTHORIZED)

        data = {}
        if request.data.get("name"):
            data['name'] = request.data.get("name")
        if request.data.get("description"):
            data['description'] = request.data.get("description")
        if request.data.get("price"):
            data['price'] = request.data.get("price")

        serializer = ProductSerializer(product, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated, IsRestaurant])
    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'product': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if product.restaurant.pk != user.pk:
            return Response({'response': "You don't have permission to delete that."},
                            status=status.HTTP_401_UNAUTHORIZED)

        operation = product.delete()
        if operation:
            return Response()
        else:
            return Response({'response': "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




