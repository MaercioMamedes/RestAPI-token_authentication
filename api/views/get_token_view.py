from api.serializers.login_serializer import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib import auth


class CustomAuthToken(ObtainAuthToken):
    """create or fetch a token from a registered user"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if auth.authenticate(username=username, password=password):
                user = User.objects.get_by_natural_key(username)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })

            else:
                return Response({"detail": "username or password invalids"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            Response({"detail": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)