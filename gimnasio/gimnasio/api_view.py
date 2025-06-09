from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Clase
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError
from .utils import enviar_notificacion_email

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def actualizar_foto_perfil(request):
    usuario = request.user
    foto = request.FILES.get('foto_perfil')

    if not foto:
        return Response({'error': 'No se ha enviado ninguna foto'}, status=400)

    usuario.foto_perfil = foto
    usuario.save()

    serializer = UsuarioSerializer(usuario, context={'request': request})
    return Response(serializer.data, status=200)

#------------------------------------------CLASE----------------------------------------------------

@api_view(['GET'])
def obtener_clase(request):
    clases = Clase.objects.all()
    serializer = ClaseSerializer(clases, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_clase_id(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
        serializer = ClaseSerializer(clase, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def crear_clase(request):
    if request.user.rol != 'monitor':
        return Response({'error': 'Permiso denegado. Solo los monitores pueden crear clases.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ClaseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(usuario=request.user)
        return Response("Clase creada", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def editar_clase(request, clase_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden editar clases.'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para modificar esta clase.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ClaseSerializer(instance=clase, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response("Clase editada", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_clase_parcial(request, clase_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden modificar clases.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para modificar esta clase.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ClaseSerializer(instance=clase, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response("Clase actualizada parcialmente", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_clase(request, clase_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden eliminar clases.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para eliminar esta clase.'}, status=status.HTTP_403_FORBIDDEN)

    clase.delete()
    return Response("Clase eliminada correctamente", status=status.HTTP_200_OK)



#------------------------------------------HORARIO----------------------------------------------------

@api_view(['GET'])
def obtener_horarios(request):
    horarios = Horario.objects.all()
    serializer = HorarioSerializer(horarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_horario_id(request, horario_id):
    try:
        horario = Horario.objects.get(id=horario_id)
        serializer = HorarioSerializer(horario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Horario.DoesNotExist:
        return Response({'error': 'Horario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_horario(request):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden crear horarios.'}, status=403)

    serializer = HorarioSerializer(data=request.data)
    if serializer.is_valid():
        try:
            horario = serializer.save()
            return Response(HorarioSerializer(horario).data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_horario(request, horario_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden editar horarios.'}, status=403)

    try:
        horario = Horario.objects.get(id=horario_id)
    except Horario.DoesNotExist:
        return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = HorarioSerializer(instance=horario, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Horario editado", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_horario_parcial(request, horario_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden actualizar horarios.'}, status=403)

    try:
        horario = Horario.objects.get(id=horario_id)
    except Horario.DoesNotExist:
        return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = HorarioSerializer(instance=horario, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Horario actualizado parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_horario(request, horario_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden eliminar horarios.'}, status=403)

    try:
        horario = Horario.objects.get(id=horario_id)
    except Horario.DoesNotExist:
        return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        horario.delete()
        return Response("Horario eliminado correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
#------------------------------------------PUBLICACIÓN----------------------------------------------------

@api_view(['GET'])
def obtener_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    serializer = PublicacionSerializer(publicaciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_publicacion_id(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
        serializer = PublicacionSerializer(publicacion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def crear_publicacion(request):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden crear publicaciones.'}, status=403)

    clase_id = request.data.get('clase')
    if not clase_id:
        return Response({'error': 'Clase requerida'}, status=400)

    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=404)

    if clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para publicar en esta clase.'}, status=403)

    serializer = PublicacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Publicación creada", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def editar_publicacion(request, publicacion_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden editar publicaciones.'}, status=403)

    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada'}, status=404)

    if publicacion.clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para editar esta publicación.'}, status=403)

    serializer = PublicacionSerializer(publicacion, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Publicación editada", status=200)
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def actualizar_publicacion_parcial(request, publicacion_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden modificar publicaciones.'}, status=403)

    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada'}, status=404)

    if publicacion.clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para editar esta publicación.'}, status=403)

    serializer = PublicacionSerializer(publicacion, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response("Publicación actualizada parcialmente", status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_publicacion(request, publicacion_id):
    if request.user.rol != 'monitor':
        return Response({'error': 'Solo los monitores pueden eliminar publicaciones.'}, status=403)

    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada'}, status=404)

    if publicacion.clase.usuario != request.user:
        return Response({'error': 'No tienes permiso para eliminar esta publicación.'}, status=403)

    publicacion.delete()
    return Response("Publicación eliminada correctamente", status=200)


#------------------------------------------SUSCRIPCIÓN----------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_suscripciones(request):
    if request.user.rol == 'cliente':
        suscripciones = Suscripcion.objects.filter(usuario=request.user)
    else:
        suscripciones = Suscripcion.objects.all()

    serializer = SuscripcionSerializer(suscripciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_suscripcion_id(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({'error': 'Suscripción no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and suscripcion.usuario != request.user:
        return Response({'error': 'No tienes permiso para ver esta suscripción.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = SuscripcionSerializer(suscripcion)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_suscripcion(request):
    if request.user.rol != 'cliente':
        return Response({'error': 'Solo los clientes pueden crear suscripciones.'}, status=403)

    serializer = SuscripcionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción creada", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_suscripcion(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and suscripcion.usuario != request.user:
        return Response({'error': 'No puedes editar esta suscripción.'}, status=403)

    serializer = SuscripcionSerializer(instance=suscripcion, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción editada", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_suscripcion_parcial(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and suscripcion.usuario != request.user:
        return Response({'error': 'No puedes modificar esta suscripción.'}, status=403)

    serializer = SuscripcionSerializer(instance=suscripcion, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción actualizada parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_suscripcion(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and suscripcion.usuario != request.user:
        return Response({'error': 'No puedes eliminar esta suscripción.'}, status=403)

    try:
        suscripcion.delete()
        return Response("Suscripción eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#------------------------------------------PAGO----------------------------------------------------    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_pagos(request):
    if request.user.rol == 'cliente':
        pagos = Pago.objects.filter(suscripcion__usuario=request.user)
    else:
        pagos = Pago.objects.all()

    serializer = PagoSerializer(pagos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_pago_id(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and pago.suscripcion.usuario != request.user:
        return Response({'error': 'No tienes acceso a este pago.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = PagoSerializer(pago)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_pago(request):
    print("Se ha recibido un intento de crear un pago desde el frontend.")
    if request.user.rol != 'cliente':
        return Response({'error': 'Solo los clientes pueden registrar pagos.'}, status=403)

    # Buscar suscripción existente
    suscripcion = Suscripcion.objects.filter(usuario=request.user).order_by('-fecha_suscripcion').first()

    # Si no hay suscripción o está cancelada/expirada, crear o reactivar
    if not suscripcion or suscripcion.estado != 'activa':
        if suscripcion:
            suscripcion.estado = 'activa'
            suscripcion.save()
        else:
            suscripcion = Suscripcion.objects.create(usuario=request.user, estado='activa')

    # Crear el pago asociado
    pago = Pago.objects.create(
        suscripcion=suscripcion,
        estado='completado',
        cantidad=10.0
    )

    return Response({
        'mensaje': 'Pago registrado y suscripción activada.',
        'pago_id': pago.id,
        'suscripcion_id': suscripcion.id
    }, status=status.HTTP_201_CREATED)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_pago(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and pago.suscripcion.usuario != request.user:
        return Response({'error': 'No tienes permiso para editar este pago.'}, status=403)

    serializer = PagoSerializer(instance=pago, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Pago editado", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_pago_parcial(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and pago.suscripcion.usuario != request.user:
        return Response({'error': 'No tienes permiso para modificar este pago.'}, status=403)

    serializer = PagoSerializer(instance=pago, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Pago actualizado parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_pago(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and pago.suscripcion.usuario != request.user:
        return Response({'error': 'No tienes permiso para eliminar este pago.'}, status=403)

    try:
        pago.delete()
        return Response("Pago eliminado correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#------------------------------------------inscripciones clase----------------------------------------------------    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_inscripciones(request):
    if request.user.rol == 'cliente':
        inscripciones = InscripcionClase.objects.filter(usuario=request.user)
    else:
        inscripciones = InscripcionClase.objects.all()

    serializer = InscripcionClaseSerializer(inscripciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_inscripcion_id(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({'error': 'Inscripción no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and inscripcion.usuario != request.user:
        return Response({'error': 'No tienes acceso a esta inscripción.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = InscripcionClaseSerializer(inscripcion)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_inscripcion(request):
    if request.user.rol != 'cliente':
        return Response({'error': 'Solo los clientes pueden inscribirse a clases.'}, status=403)

    suscripcion = Suscripcion.objects.filter(usuario=request.user, estado='activa').first()
    if not suscripcion:
        return Response({'error': 'Debes tener una suscripción activa para inscribirte a clases.'}, status=403)

    data = request.data.copy()
    data['usuario'] = request.user.id  # Aseguramos que la inscripción se haga como cliente actual
    serializer = InscripcionClaseSerializer(data=data)

    if serializer.is_valid():
        try:
            serializer.save()

            inscripcion = serializer.instance
            clase = inscripcion.clase
            usuario = inscripcion.usuario

            mensaje = f'Te has inscrito correctamente en la clase "{clase.nombre}". ¡Nos vemos pronto!'
            enviar_notificacion_email('Inscripción confirmada', mensaje, usuario.email)

            return Response("Inscripción creada", status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_inscripcion(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and inscripcion.usuario != request.user:
        return Response({'error': 'No puedes modificar esta inscripción.'}, status=403)

    serializer = InscripcionClaseSerializer(instance=inscripcion, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Inscripción editada", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_inscripcion_parcial(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and inscripcion.usuario != request.user:
        return Response({'error': 'No puedes modificar esta inscripción.'}, status=403)

    serializer = InscripcionClaseSerializer(instance=inscripcion, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Inscripción actualizada parcialmente", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_inscripcion(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.user.rol == 'cliente' and inscripcion.usuario != request.user:
        return Response({'error': 'No puedes eliminar esta inscripción.'}, status=403)

    try:
        clase = inscripcion.clase
        usuario = inscripcion.usuario

        mensaje = f'Has cancelado tu inscripción a la clase "{clase.nombre}". Esperamos verte pronto en otra clase.'
        enviar_notificacion_email('Inscripción cancelada', mensaje, usuario.email)

        inscripcion.delete()
        return Response("Inscripción eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------------------------------------------inscripciones clase----------------------------------------------------    

@api_view(['GET'])
def obtener_comentarios(request, publicacion_id):
    comentarios = Comentario.objects.filter(publicacion_id=publicacion_id).order_by('-fecha_comentario')
    serializer = ComentarioSerializer(comentarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_comentario(request):
    data = request.data.copy()
    serializer = ComentarioSerializer(data=data)
    if serializer.is_valid():
        serializer.save(usuario=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_dislike_comentario(request, comentario_id):
    tipo = request.data.get('tipo')
    if tipo not in ['like', 'dislike']:
        return Response({'error': 'Tipo inválido'}, status=400)

    comentario = Comentario.objects.get(id=comentario_id)
    like, creado = LikeComentario.objects.get_or_create(comentario=comentario, usuario=request.user)
    if not creado and like.tipo == tipo:
        like.delete()
        return Response({'mensaje': f'{tipo} eliminado'}, status=200)
    else:
        like.tipo = tipo
        like.save()
        return Response({'mensaje': f'{tipo} actualizado'}, status=200)

#------------------------------------------categorias clase----------------------------------------------------    

@api_view(['GET'])
def obtener_categorias_clase(request):
    categorias = CategoriaClase.objects.all()
    serializer = CategoriaClaseSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_clases_por_categoria(request, categoria_slug):
    try:
        categoria = CategoriaClase.objects.get(slug=categoria_slug)
    except CategoriaClase.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=404)

    clases = Clase.objects.filter(categoria=categoria)
    clases_serializadas = ClaseSerializer(clases, many=True, context={'request': request})

    monitores = set(clase.usuario for clase in clases)
    monitores_serializados = UsuarioSerializer(monitores, many=True, context={'request': request})

    return Response({
        'categoria': categoria.nombre,
        'clases': clases_serializadas.data,
        'monitores': monitores_serializados.data
    })


#------------------------------------------reserva horario----------------------------------------------------   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservar_horario(request, horario_id):
    usuario = request.user
    try:
        horario = Horario.objects.get(id=horario_id)
        clase = horario.clase
    except Horario.DoesNotExist:
        return Response({'error': 'Horario no encontrado'}, status=404)

    if not InscripcionClase.objects.filter(usuario=usuario, clase=clase, estado='activa').exists():
        return Response({'error': 'Debes estar inscrito en la clase para reservar.'}, status=403)

    if horario.reservas.count() >= clase.cupo_maximo:
        return Response({'error': 'No hay cupo disponible en este horario.'}, status=400)

    reserva, creada = ReservaHorario.objects.get_or_create(usuario=usuario, horario=horario)
    if not creada:
        return Response({'error': 'Ya tienes una reserva en este horario.'}, status=400)

    return Response({'mensaje': 'Reserva realizada correctamente.'}, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelar_reserva(request, horario_id):
    usuario = request.user
    try:
        reserva = ReservaHorario.objects.get(usuario=usuario, horario_id=horario_id)
        reserva.delete()
        return Response({'mensaje': 'Reserva cancelada correctamente.'}, status=200)
    except ReservaHorario.DoesNotExist:
        return Response({'error': 'No tienes reserva en este horario.'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_reservas_horario(request, horario_id):
    try:
        reservas = ReservaHorario.objects.filter(horario_id=horario_id)
        return Response({'reservas': reservas.count()}, status=200)
    except Horario.DoesNotExist:
        return Response({'error': 'Horario no encontrado'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tiene_reserva_horario(request, horario_id):
    usuario = request.user
    reservado = ReservaHorario.objects.filter(usuario=usuario, horario_id=horario_id).exists()
    return Response({'reservado': reservado}, status=200)