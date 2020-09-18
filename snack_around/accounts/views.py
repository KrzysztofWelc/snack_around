from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, UserSerializer, RestaurantImageSerializer
from .permissions import IsRestaurant
from .models import RestaurantImage


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


@api_view(['GET'])
@permission_classes([])
def single_restaurant_view(request, pk):
    user = get_user_model()
    try:
        restaurant = user.objects.get(pk=pk, is_restaurant=True)
    except user.DoesNotExist:
        return Response({'user': 'user not found'})

    data = UserSerializer(restaurant).data

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_profile(request):
    user = request.user
    data = UserSerializer(user).data

    return Response(data)


class ImageView(APIView):
    parser_classes = (FormParser, MultiPartParser,)
    permission_classes = (IsAuthenticated, IsRestaurant)

    def post(self, request, *args, **kwargs):

        data = [{'image': _file, 'info': request.user.info.pk} for _file in request.FILES.getlist('images')]
        file_serializer = RestaurantImageSerializer(data=data, many=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        img_id = kwargs.get('pk')
        try:
            image = RestaurantImage.objects.get(pk=img_id)
        except RestaurantImage.DoesNotExist:
            return Response({'image': 'image not found'}, status=status.HTTP_404_NOT_FOUND)

        if image.info != request.user.info:
            return Response({'response': "You don't have permission to delete that."},
                            status=status.HTTP_401_UNAUTHORIZED)

        operation = image.delete()
        if operation:
            return Response()
        else:
            return Response({'response': "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', ])
@permission_classes([])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = RegistrationSerializer(user).data
        data['token'] = Token.objects.get(user=user).key
    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET', ])
@permission_classes([])
def restaurant_images_view(request, user_id):
    user_model = get_user_model()
    try:
        images = user_model.objects.get(pk=user_id).info.images.all()
    except user_model.DoesNotExist:
        return Response({'detail': ['no user found', ]})

    data = RestaurantImageSerializer(instance=images, many=True).data

    return Response({'images': data})
