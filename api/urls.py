from rest_framework.routers import SimpleRouter
from django.urls import path
from api.views.register_viewset import RegisterViewSet
from api.views.get_token_view import CustomAuthToken


router = SimpleRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = router.urls

urlpatterns += [
    path('token/', CustomAuthToken.as_view(), name='token')
]
