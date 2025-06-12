from django.urls import path
from . import api_view
from .registro_views import register_usuario, CustomTokenObtainPairView

urlpatterns = [
    #usuario
    path('usuario/foto_perfil/', api_view.actualizar_foto_perfil, name='actualizar_foto_perfil'),
    
    #clases
    path('clases/', api_view.obtener_clase, name='obtener_clase'),
    path('clases/<int:clase_id>/', api_view.obtener_clase_id, name='obtener_clase_id'),
    path('clases/crear/', api_view.crear_clase, name='crear_clase'),
    path('clases/editar/<int:clase_id>/', api_view.editar_clase, name='editar_clase'),
    path('clases/actualizar/<int:clase_id>/', api_view.actualizar_clase_parcial, name='actualizar_clase_parcial'),
    path('clases/eliminar/<int:clase_id>/', api_view.eliminar_clase, name='eliminar_clase'),
    
    #categorías
    path('categorias_clase/', api_view.obtener_categorias_clase, name='obtener_categorias_clase'),
    path('categorias/<slug:categoria_slug>/clases/', api_view.obtener_clases_por_categoria, name='obtener_clases_por_categoria'),
    path('categorias/<int:categoria_id>/', api_view.obtener_categoria, name='obtener_categoria'),
    path('categorias/crear/', api_view.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', api_view.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', api_view.eliminar_categoria, name='eliminar_categoria'),


    #horario
    path('horarios/', api_view.obtener_horarios),
    path('horarios/<int:horario_id>/', api_view.obtener_horario_id),
    path('horarios/crear/', api_view.crear_horario),
    path('horarios/editar/<int:horario_id>/', api_view.editar_horario),
    path('horarios/actualizar/<int:horario_id>/', api_view.actualizar_horario_parcial),
    path('horarios/eliminar/<int:horario_id>/', api_view.eliminar_horario),
    
    #publicación
    path('publicaciones/', api_view.obtener_publicaciones, name='obtener_publicaciones'),
    path('publicaciones/<int:publicacion_id>/', api_view.obtener_publicacion_id, name='obtener_publicacion_id'),
    path('publicaciones/crear/', api_view.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/editar/<int:publicacion_id>/', api_view.editar_publicacion, name='editar_publicacion'),
    path('publicaciones/actualizar/<int:publicacion_id>/', api_view.actualizar_publicacion_parcial, name='actualizar_publicacion_parcial'),
    path('publicaciones/eliminar/<int:publicacion_id>/', api_view.eliminar_publicacion, name='eliminar_publicacion'),
    
    #suscripción
    path('suscripciones/', api_view.obtener_suscripciones, name='obtener_suscripciones'),
    path('suscripciones/<int:suscripcion_id>/', api_view.obtener_suscripcion_id, name='obtener_suscripcion_id'),
    path('suscripciones/crear/', api_view.crear_suscripcion, name='crear_suscripcion'),
    path('suscripciones/editar/<int:suscripcion_id>/', api_view.editar_suscripcion, name='editar_suscripcion'),
    path('suscripciones/actualizar/<int:suscripcion_id>/', api_view.actualizar_suscripcion_parcial, name='actualizar_suscripcion_parcial'),
    path('suscripciones/eliminar/<int:suscripcion_id>/', api_view.eliminar_suscripcion, name='eliminar_suscripcion'),
    
    #pagos
    path('pagos/', api_view.obtener_pagos, name='obtener_pagos'),
    path('pagos/<int:pago_id>/', api_view.obtener_pago_id, name='obtener_pago_id'),
    path('pagos/crear/', api_view.crear_pago, name='crear_pago'),
    path('pagos/editar/<int:pago_id>/', api_view.editar_pago, name='editar_pago'),
    path('pagos/actualizar/<int:pago_id>/', api_view.actualizar_pago_parcial, name='actualizar_pago_parcial'),
    path('pagos/eliminar/<int:pago_id>/', api_view.eliminar_pago, name='eliminar_pago'),
    
    #incripcion clase
    path('inscripciones/', api_view.obtener_inscripciones, name='obtener_inscripciones'),
    path('inscripciones/<int:inscripcion_id>/', api_view.obtener_inscripcion_id, name='obtener_inscripcion_id'),
    path('inscripciones/crear/', api_view.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/editar/<int:inscripcion_id>/', api_view.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/actualizar/<int:inscripcion_id>/', api_view.actualizar_inscripcion_parcial, name='actualizar_inscripcion_parcial'),
    path('inscripciones/eliminar/<int:inscripcion_id>/', api_view.eliminar_inscripcion, name='eliminar_inscripcion'),
    
    # registro
    path('usuarios/registrar_usuario/', register_usuario, name='registrar_usuario'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    #comentario
    path('comentarios/<int:publicacion_id>/', api_view.obtener_comentarios),
    path('comentarios/crear/', api_view.crear_comentario),
    path('comentarios/<int:comentario_id>/like_dislike_comentario/', api_view.like_dislike_comentario),

    #reservas
    path('reservas/<int:horario_id>/crear/', api_view.reservar_horario, name='reservar_horario'),
    path('reservas/<int:horario_id>/cancelar/', api_view.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/<int:horario_id>/contador/', api_view.ver_reservas_horario, name='ver_reservas_horario'),
    path('reservas/<int:horario_id>/', api_view.tiene_reserva_horario),
    
]
