from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions_helper import AdminPermission

from .serializers import CustomJWTSerializer, SignupSerializer


class JWTLoginView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
    permission_classes = (AllowAny,)


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (IsAuthenticated, AdminPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_201_CREATED)
