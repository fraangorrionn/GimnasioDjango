from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol']

class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'
        
class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

    def validate(self, data):
        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        if hora_fin <= hora_inicio:
            raise serializers.ValidationError("La hora de fin debe ser mayor que la hora de inicio.")

        return data

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

class InscripcionClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscripcionClase
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=InscripcionClase.objects.all(),
                fields=['usuario', 'clase'],
                message="El usuario ya está inscrito en esta clase."
            )
        ]
        
class ImagenClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenClase
        fields = ['id', 'clase', 'imagen', 'descripcion', 'fecha_subida']

class ComentarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'publicacion', 'usuario', 'usuario_nombre', 'contenido', 'fecha']

        
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)