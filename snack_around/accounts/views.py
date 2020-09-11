from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, UserSerializer


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
