from rest_framework.viewsets import ModelViewSet
from api.serializers.register_serializer import RegisterSerializer
from api.serializers.register_update import RegisterUpdateSerializer
from register.models import Register
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


class RegisterViewSet(ModelViewSet):
    """Views set for class Register"""

    queryset = Register.objects.all()
    http_method_names = ['get', 'put', 'patch', 'post', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """assign authentication exception to create resource"""

        if self.action in ('create',):
            self.permission_classes = [AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def get_serializer(self, *args, **kwargs):
        """getting serializer according to the request type"""

        if self.request.method == 'POST':
            serializer = RegisterSerializer(data=self.request.data)
            return serializer

        else:
            serializer = RegisterUpdateSerializer(data=self.request.data)
            return serializer

    def create(self, request, *args, **kwargs):
        """Create New resource"""
        # This method does not need authentication

        serializer = self.get_serializer()

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['fullname'].split()[0]
            password = serializer.validated_data['password']

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
            )

            user.set_password(password)

            register = Register.objects.create(
                fullname=serializer.validated_data['fullname'],
                phone=serializer.validated_data['phone'],
                user=user
            )

            return Response(
                {
                    "fullname": register.fullname,
                    "username": register.user.username,
                    "email": register.user.email,
                }
            )

    def list(self, request, *args, **kwargs):
        """list all objects of the Register class"""

        def format_register(list_registers):
            registers_formatted = []

            for register in list_registers:
                dict_register = register.__dict__
                del dict_register['_state']
                user = User.objects.get(pk=dict_register['user_id'])
                dict_register['email'] = user.email
                registers_formatted.append(dict_register)

            return registers_formatted

        return Response(format_register(self.queryset))

    def update(self, request, *args, **kwargs):
        """updates all fields of a Register class object, except the password"""

        serializer = self.get_serializer()

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            fullname = serializer.validated_data['fullname']
            first_name = serializer.validated_data['fullname'].split()[0]

            register = Register.objects.get(pk=kwargs['pk'])
            register.fullname = fullname
            register.user.email = email
            register.user.username = username
            register.user.first_name = first_name

            register.user.save()
            register.save()

            return Response(
                {
                    "id": register.id,
                    "fullname": register.fullname,
                    "username": register.user.username,
                    "email": register.user.email,
                    "phone": register.phone,
                    "user_id": register.user.id
                }
            )

    def partial_update(self, request, *args, **kwargs):
        """partial updates of Register class fields, except password"""

        serializer = self.get_serializer()
        register = Register.objects.get(pk=kwargs['pk'])

        if serializer.is_valid():
            if 'fullname' in serializer.validated_data:
                register.fullname = serializer.validated_data['fullname']
                register.save()
                register.user.first_name = serializer.validated_data['fullname'].split()[0]
                register.user.save()

            if 'phone' in serializer.validated_data:
                register.phone = serializer.validated_data['phone']
                register.save()

            if 'email' in serializer.validated_data:
                register.user.email = serializer.validated_data['email']
                register.user.save()

            if 'username' in serializer.validated_data:
                register.user.username = serializer.validated_data['username']
                register.user.save()

            return Response(
                {
                    "id": register.id,
                    "fullname": register.fullname,
                    "username": register.user.username,
                    "email": register.user.email,
                    "phone": register.phone,
                    "user_id": register.user.id
                }
            )

    def destroy(self, request, *args, **kwargs):
        """deletes object from Register class by ID"""

        register = Register.objects.get(pk=kwargs['pk'])
        register.user.delete()

        return Response({"detail": "Register deleted"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """retrieve object from Register class by ID"""

        register = Register.objects.get(pk=kwargs['pk'])

        return Response(
            {
                "id": register.id,
                "fullname": register.fullname,
                "username": register.user.username,
                "email": register.user.email,
                "phone": register.phone,
                "user_id": register.user.id
            },
            status=status.HTTP_200_OK
        )
