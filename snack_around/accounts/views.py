from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationSerializer, RestaurantInfoSerializer


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


@api_view(['POST', ])
@permission_classes([])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['id'] = account.id
        data['email'] = account.email
        data['username'] = account.username
        data['is_restaurant'] = account.is_restaurant
        data['token'] = Token.objects.get(user=account).key
        if data['is_restaurant']:
            data['restaurant_info'] = {}
            data['restaurant_info']['address'] = account.info.address
            data['restaurant_info']['phone_num'] = account.info.phone_num
    else:
        data = serializer.errors
    return Response(data)
