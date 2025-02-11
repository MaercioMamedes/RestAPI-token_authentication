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

    def test_get_token(self):
        response = self.client.post(self.url, {"username": "user01", "password": "1234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)

    def test_when_user_enters_incorrect_password_or_username_returns_error_401(self):
        response = self.client.post(self.url, {"username": "user01", "password": "234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_user_enters_invalid_data_it_returns_error_400(self):
        response = self.client.post(self.url, {"data": "user01", "invalid": "234"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_user_accesses_register_list_without_authentication_returns_error_401(self):
        response = self.client.get(f'{self.url_register}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_user_accesses_register_by_ID_without_authentication_it_returns_401(self):
        response = self.client.get(f'{self.url_register}1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_user_tries_to_update_without_authentication_it_returns_error_401(self):
        response = self.client.put(f'{self.url_register}1/',
                                   data={
                                       'fullname': 'Novo Teste',
                                       'username': 'novo01',
                                       'phone': '9888566565',
                                       'email': 'novo@novo',
                                   },
                                   format='json'
                                   )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_user_tries_to_partial_update_without_authentication_it_returns_error_401(self):
        response = self.client.patch(f'{self.url_register}1/',
                                     data={
                                         'fullname': 'Novo Teste',
                                         'username': 'novo01',
                                     },
                                     format='json'
                                     )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_when_use_tries_to_delete_resource_without_being_authenticated_it_returns_error_401(self):
        response = self.client.delete(f'{self.url_register}1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
