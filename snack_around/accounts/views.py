from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer


@api_view(['POST', ])
@permission_classes([])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'registration successful'
        data['email'] = account.email
        data['username'] = account.username
        data['token'] = Token.objects.get(user=account).key
    else:
        data = serializer.errors
    return Response(data)
