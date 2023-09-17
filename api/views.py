from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from api.register_serializer import RegisterSerializer
from api.login_serializer import LoginSerializer
from register.models import Register
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegisterViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            register = Register.objects.create(
                name=serializer.validated_data['name'],
                phone=serializer.validated_data['phone'],
            )

            return Response({'name': register.name, 'phone': register.phone})

    def list(self, request, *args, **kwargs):
        return Response('teste')


class ViewTest(APIView):

    def get(self, request):
        return Response("funcionou")


class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get_by_natural_key(username)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
