from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify

class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('monitor', 'Monitor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

class Suscripcion(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('expirada', 'Expirada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    fecha_suscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)

class Pago(models.Model):
    ESTADOS = (
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('fallido', 'Fallido'),
    )
    suscripcion = models.OneToOneField(Suscripcion, on_delete=models.CASCADE, related_name='pago')
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS)

class CategoriaClase(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Clase(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clases')  # solo monitores
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(CategoriaClase, on_delete=models.SET_NULL, null=True, related_name='clases')
    cupo_maximo = models.IntegerField()
    imagen = models.ImageField(upload_to='clases/', null=True, blank=True)


class Horario(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class Publicacion(models.Model):
    clase = models.ForeignKey('Clase', on_delete=models.CASCADE, related_name='publicaciones')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True) 

class InscripcionClase(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)

    class Meta:
        unique_together = ('usuario', 'clase')

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

class LikeComentario(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    class Meta:
        unique_together = ('comentario', 'usuario')

class ReservaHorario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'horario')

