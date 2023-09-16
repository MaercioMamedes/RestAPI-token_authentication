from rest_framework.viewsets import ModelViewSet
from api.register_serializer import RegisterSerializer
from register.models import Register


class RegisterViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']

