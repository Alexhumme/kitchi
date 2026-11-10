from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import AuthResponseSerializer, LoginSerializer, MeSerializer, RegisterSerializer


def _token_payload(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {"token": token.key, "user": MeSerializer(user).data}


@extend_schema(request=RegisterSerializer, responses={201: AuthResponseSerializer})
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Alta de cuenta y entrega inmediata de token (AC-06)."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(_token_payload(serializer.save()), status=status.HTTP_201_CREATED)


@extend_schema(request=LoginSerializer, responses={200: AuthResponseSerializer})
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(request, **serializer.validated_data)
    if user is None:
        return Response(
            {"error": {"code": "INVALID_CREDENTIALS", "message": "Usuario o contraseña incorrectos.", "details": {}}},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return Response(_token_payload(user))


@extend_schema(request=None, responses={204: None})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """Invalida el token presentado; al volver a iniciar sesión se genera uno nuevo."""
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses=MeSerializer)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data)
