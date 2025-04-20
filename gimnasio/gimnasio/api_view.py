from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Clase
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError

#------------------------------------------CLASE----------------------------------------------------

@api_view(['GET'])
def obtener_clase(request):
    clases = Clase.objects.all()
    serializer = ClaseSerializer(clases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_clase_id(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
        serializer = ClaseSerializer(clase)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def crear_clase(request):
    serializer = ClaseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Clase creada", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_clase(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({"error": "Clase no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClaseSerializer(instance=clase, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Clase editada", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def actualizar_clase_parcial(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({"error": "Clase no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClaseSerializer(instance=clase, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Clase actualizada parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_clase(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({"error": "Clase no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    try:
        clase.delete()
        return Response("Clase eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
def crear_horario(request):
    serializer = HorarioSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Horario creado", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_horario(request, horario_id):
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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def actualizar_horario_parcial(request, horario_id):
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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_horario(request, horario_id):
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
@parser_classes([MultiPartParser, FormParser]) # Permite recibir imágenes u otros archivos vía multipart/form-data
def crear_publicacion(request):
    serializer = PublicacionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Publicación creada", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def editar_publicacion(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({"error": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PublicacionSerializer(instance=publicacion, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Publicación editada", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@parser_classes([MultiPartParser, FormParser])
def actualizar_publicacion_parcial(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({"error": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PublicacionSerializer(instance=publicacion, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Publicación actualizada parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_publicacion(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({"error": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    try:
        publicacion.delete()
        return Response("Publicación eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#------------------------------------------SUSCRIPCIÓN----------------------------------------------------

@api_view(['GET'])
def obtener_suscripciones(request):
    suscripciones = Suscripcion.objects.all()
    serializer = SuscripcionSerializer(suscripciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_suscripcion_id(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
        serializer = SuscripcionSerializer(suscripcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Suscripcion.DoesNotExist:
        return Response({'error': 'Suscripción no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def crear_suscripcion(request):
    serializer = SuscripcionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción creada", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_suscripcion(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SuscripcionSerializer(instance=suscripcion, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción editada", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def actualizar_suscripcion_parcial(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SuscripcionSerializer(instance=suscripcion, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Suscripción actualizada parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_suscripcion(request, suscripcion_id):
    try:
        suscripcion = Suscripcion.objects.get(id=suscripcion_id)
    except Suscripcion.DoesNotExist:
        return Response({"error": "Suscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    try:
        suscripcion.delete()
        return Response("Suscripción eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#------------------------------------------PAGO----------------------------------------------------    

@api_view(['GET'])
def obtener_pagos(request):
    pagos = Pago.objects.all()
    serializer = PagoSerializer(pagos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_pago_id(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
        serializer = PagoSerializer(pago)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pago.DoesNotExist:
        return Response({'error': 'Pago no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def crear_pago(request):
    serializer = PagoSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Pago registrado", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_pago(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PagoSerializer(instance=pago, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Pago editado", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def actualizar_pago_parcial(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PagoSerializer(instance=pago, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Pago actualizado parcialmente", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_pago(request, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        pago.delete()
        return Response("Pago eliminado correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#------------------------------------------inscripciones clase----------------------------------------------------    


@api_view(['GET'])
def obtener_inscripciones(request):
    inscripciones = InscripcionClase.objects.all()
    serializer = InscripcionClaseSerializer(inscripciones, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_inscripcion_id(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
        serializer = InscripcionClaseSerializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except InscripcionClase.DoesNotExist:
        return Response({'error': 'Inscripción no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def crear_inscripcion(request):
    serializer = InscripcionClaseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Inscripción creada", status=status.HTTP_201_CREATED)
        except IntegrityError: #manejar errores por inscripciones duplicadas
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editar_inscripcion(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InscripcionClaseSerializer(instance=inscripcion, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Inscripción editada", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def actualizar_inscripcion_parcial(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InscripcionClaseSerializer(instance=inscripcion, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Inscripción actualizada parcialmente", status=status.HTTP_200_OK)
        except IntegrityError:
            return Response("El usuario ya está inscrito en esta clase", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_inscripcion(request, inscripcion_id):
    try:
        inscripcion = InscripcionClase.objects.get(id=inscripcion_id)
    except InscripcionClase.DoesNotExist:
        return Response({"error": "Inscripción no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    try:
        inscripcion.delete()
        return Response("Inscripción eliminada correctamente", status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#------------------------------------------imagen clase----------------------------------------------------  
    
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def subir_imagen_clase(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        return Response({'error': 'Clase no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    datos = request.data.copy()
    datos['clase'] = clase.id
    serializer = ImagenClaseSerializer(data=datos)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------comentario publicacion----------------------------------------------------  

@api_view(['POST'])
def crear_comentario(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    datos = request.data.copy()
    datos['publicacion'] = publicacion.id
    datos['usuario'] = request.user.id

    serializer = ComentarioSerializer(data=datos)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)