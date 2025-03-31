from django.contrib import admin
from .models import Usuario, Suscripcion, Pago, Clase, Horario, Publicacion, InscripcionClase

admin.site.register(Usuario)
admin.site.register(Suscripcion)
admin.site.register(Pago)
admin.site.register(Clase)
admin.site.register(Horario)
admin.site.register(Publicacion)
admin.site.register(InscripcionClase)
