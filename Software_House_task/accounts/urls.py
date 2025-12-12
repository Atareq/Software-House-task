from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import JWTLoginView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', JWTLoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
