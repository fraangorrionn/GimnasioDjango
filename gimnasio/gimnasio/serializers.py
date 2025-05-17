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
    clase_nombre = serializers.CharField(source='clase.nombre', read_only=True)

    class Meta:
        model = Horario
        fields = ['id', 'clase', 'clase_nombre', 'dia_semana', 'hora_inicio', 'hora_fin']


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

class LikeComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComentario
        fields = ['id', 'usuario', 'tipo']

class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    usuario_data = UsuarioSerializer(source='usuario', read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'publicacion', 'usuario', 'usuario_data', 'contenido', 'fecha_comentario', 'likes', 'dislikes']


    def get_likes(self, obj):
        return obj.likes.filter(tipo='like').count()

    def get_dislikes(self, obj):
        return obj.likes.filter(tipo='dislike').count()
        
        
        
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