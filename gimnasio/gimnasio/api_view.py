from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Clase
from .serializers import ClaseSerializer

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