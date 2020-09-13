from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, UserSerializer, RestaurantImageSerializer
from .permissions import IsRestaurant


class ListRestaurantsView(ListAPIView):
    queryset = get_user_model().objects.filter(is_restaurant=True)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = []


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })


class UserView(APIView):
    permission_classes = []

    # get restaurants ONLY
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        user = get_user_model()
        try:
            restaurant = user.objects.get(pk=pk, is_restaurant=True)
        except user.DoesNotExist:
            return Response({'user': 'user not found'})

        data = UserSerializer(restaurant).data

        return Response(data)


class ImageView(APIView):
    parser_classes = (MultiPartParser, )
    permission_classes = (IsAuthenticated, IsRestaurant)

    def post(self, request, *args, **kwargs):
        data = {
            'image': request.FILES.pop('image'),
            'info': request.user.info.pk
        }
        file_serializer = RestaurantImageSerializer(data=data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = RegistrationSerializer(user).data
    else:
        data = serializer.errors
    return Response(data)
