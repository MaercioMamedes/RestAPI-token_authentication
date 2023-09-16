from rest_framework.viewsets import ModelViewSet
from api.register_serializer import RegisterSerializer
from register.models import Register
from rest_framework.response import Response


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
