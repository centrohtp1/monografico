from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Contacto
from .serializers import ContactoSerializer

@api_view(['POST'])
def crear_contacto(request):
    if request.method == 'POST':
        serializer = ContactoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def listar_contactos(request):
    if request.method == 'GET':
        contactos = Contacto.objects.all()
        serializer = ContactoSerializer(contactos, many=True)
        return Response(serializer.data)
    
@api_view(['DELETE'])
def eliminar_contacto(request, pk):
    try:
        contacto = Contacto.objects.get(pk=pk)
    except Contacto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        contacto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)