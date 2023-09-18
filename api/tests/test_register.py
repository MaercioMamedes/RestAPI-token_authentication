from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from register.models import Register
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


class AuthenticationTestCase(APITestCase):

    def setUp(self) -> None:
        def create_django_user():
            user = User.objects.create_user(username='user01', email='teste@teste', first_name='Teste')
            user.set_password('1234')
            user.save()
            return user

        self.client = APIClient()
        self.register = Register.objects.create(
            fullname="Teste Teste",
            phone="82998203433",
            user=create_django_user()
        )

        self.url = reverse("token")
        self.url_register = reverse("register-list")
        self.token = Token.objects.get_or_create(user=self.register.user)[0]

    def test_get_register_by_id(self):
        response = self.client.get(f'{self.url_register}1/', headers={
            'Authorization': f'Token {self.token.key}'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
