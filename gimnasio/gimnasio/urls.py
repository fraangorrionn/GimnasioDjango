from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clases/', views.obtener_clase, name='obtener_clase'),
    path('clases/<int:clase_id>/', views.obtener_clase_id, name='obtener_clase_id'),
    path('clases/crear/', views.crear_clase, name='crear_clase'),
    path('clases/editar/<int:clase_id>/', views.editar_clase, name='editar_clase'),
    path('clases/actualizar/<int:clase_id>/', views.actualizar_clase_parcial, name='actualizar_clase_parcial'),
    path('clases/eliminar/<int:clase_id>/', views.eliminar_clase, name='eliminar_clase'),
]