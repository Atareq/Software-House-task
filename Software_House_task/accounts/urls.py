from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import JWTLoginView, SignupView

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', JWTLoginView.as_view(), name='token_obtain_pair'),
    path('accounts/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
