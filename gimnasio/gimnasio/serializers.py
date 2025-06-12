from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    foto_perfil_url = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'foto_perfil_url']

    def get_foto_perfil_url(self, obj):
        request = self.context.get('request', None)
        if not request:
            return None
        if obj.foto_perfil and hasattr(obj.foto_perfil, 'url'):
            return request.build_absolute_uri(obj.foto_perfil.url)
        return None



class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    monitor_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    monitor_foto = serializers.SerializerMethodField()
    
    class Meta:
        model = Clase
        fields = [
            'id', 'usuario', 'nombre', 'descripcion', 'categoria', 'categoria_nombre',
            'cupo_maximo', 'imagen', 'imagen_url', 'monitor_nombre', 'monitor_foto'
        ]

    def get_monitor_foto(self, obj):
        if obj.usuario.foto_perfil and hasattr(obj.usuario.foto_perfil, 'url'):
            return obj.usuario.foto_perfil.url
        return None

    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return obj.imagen.url
        return None


class CategoriaClaseSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = CategoriaClase
        fields = ['id', 'nombre', 'slug', 'imagen', 'imagen_url']
        read_only_fields = ['slug']

    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return obj.imagen.url
        return None


        
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
        
class ReservaHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaHorario
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ReservaHorario.objects.all(),
                fields=['usuario', 'horario'],
                message="Ya tienes una reserva para este horario."
            )
        ]

        
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

    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Usuario.objects.create(**validated_data)