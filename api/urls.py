from rest_framework.routers import SimpleRouter
from django.urls import path
from api.views import RegisterViewSet, ViewTest, CustomAuthToken


router = SimpleRouter()
router.register('register', RegisterViewSet, basename='register')

urlpatterns = router.urls

urlpatterns += [
    path('teste/', ViewTest.as_view()),
    path('token/', CustomAuthToken.as_view())
]
