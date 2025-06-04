from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegistroUsuarioSerializer

Usuario = get_user_model()

@api_view(['POST'])
def register_usuario(request):
    data = request.data.copy()

    # Autogenerar username si no se envía
    if 'username' not in data or not data['username']:
        if 'email' in data:
            data['username'] = data['email'].split('@')[0]

    serializer = RegistroUsuarioSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        return token

    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        try:
            user = Usuario.objects.filter(username=username_or_email).first()
            if not user:
                user = Usuario.objects.filter(email=username_or_email).first()
            if not user or not user.check_password(password):
                raise AuthenticationFailed("Credenciales inválidas.")
        except Usuario.DoesNotExist:
            raise AuthenticationFailed("Credenciales inválidas.")

        # Reemplazamos el username por el real para que funcione el flujo
        attrs['username'] = user.username
        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
