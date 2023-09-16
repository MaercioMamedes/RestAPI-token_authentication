from rest_framework.routers import SimpleRouter
from django.urls import path
from api.views import RegisterViewSet


router = SimpleRouter()
router.register('register', RegisterViewSet, basename='register')

