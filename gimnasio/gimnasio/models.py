from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('monitor', 'Monitor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES)

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

class Clase(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clases')  # solo monitores
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)
    cupo_maximo = models.IntegerField()

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


class ImagenClase(models.Model):
    clase = models.ForeignKey('Clase', on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='clases/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.clase.nombre} ({self.id})"

class Comentario(models.Model):
    publicacion = models.ForeignKey('Publicacion', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.publicacion.titulo}"
