from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from rest_framework import status
from .serializer import  CreateVendedorSerializer, GetVendedoresSerializer, GetVendedoreSerializer, UpdateVendedorSerilizer, GetClientesSerializer, UpdateClienteSerializer, UserCreateSerializer, GetUsersSerializer, EmpresaAdminCreateSerializer,GetAdminSerializer



# Esta api es para crear usuarios con rol 'Cliente'
@api_view(['POST'])
def create_user(request): 
    serializer = UserCreateSerializer(data=request.data)  # Usa el serializer correcto
    if serializer.is_valid():
        if serializer.validated_data.get('rol') == 'Cliente':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "El rol debe ser 'cliente' para crear un cliente."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Esta api es para obtener todos los usuarios
@api_view(['GET'])
def get_users(request):
    users = models.user.objects.all()
    serializer = GetUsersSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 


# Esta api es para actualizar los datos de un cliente
@api_view(['PUT'])
def update_cliente(request, id):
    try:
        cliente = models.cliente.objects.get(id_cliente=id)
    except models.cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateClienteSerializer(cliente, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Esta api es para obtener todos los clientes
@api_view(['GET'])
def list_clientes(request):
    clientes = models.cliente.objects.all()
    serializer = GetClientesSerializer(clientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Esta api es para eliminar un cliente
@api_view(['DELETE'])
def delete_cliente(request, id):
    try:
        cliente = models.cliente.objects.get(id_cliente=id)
    except models.cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    cliente.delete()
    return Response({"mensaje": "Cliente eliminado correctamente."}, status=status.HTTP_200_OK)

#Esta api es para actualizar los datos de un usuario
@api_view(['PUT'])
def update_user(request):
    serializer = UpdateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Esta api es para crear usuarios con rol 'Admin'
@api_view(['POST'])
def create_empresa_admin(request):
    serializer = EmpresaAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data.get('rol') == 'Admin':
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "El rol debe ser 'Admin' para crear un administrador de empresa."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Esta api es para obtener todos los administradores de empresa
@api_view(['GET'])
def list_admins(request):
    admins = models.empresaAdmin.objects.all()  # Cambia aquí
    serializer = GetAdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



#Esta api es para eliminar un administrador de empresa
@api_view(['DELETE'])
def delete_admin(request, id):
    try:
        admin = models.user.objects.get(id=id, rol="Admin")
    except models.user.DoesNotExist:
        return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    admin.delete()
    return Response({"mensaje": "Administrador eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


#Esta api es para crear vendedores
@api_view(['POST'])
def create_vendedor(request):
    serializer = CreateVendedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Esta api es para obtener todos los vendedores
@api_view(['GET'])
def list_vendedores(request):
    vendedores = models.vendedor.objects.all()
    serializer = GetVendedoresSerializer(vendedores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



#Esta api es para obtener un vendedor por id
@api_view(['GET'])
def get_vendedor(request, id):
    try:
        vendedor = models.vendedor.objects.get(id_vendedor=id)
    except models.vendedor.DoesNotExist:
        return Response({"error": "Vendedor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = GetVendedoreSerializer(vendedor)
    return Response(serializer.data, status=status.HTTP_200_OK)




#Esta api es para actualizar los datos de un vendedor
@api_view(['PUT'])
def update_vendedor(request, id):
    try:
        vendedor = models.vendedor.objects.get(id_vendedor=id)
    except models.vendedor.DoesNotExist:
        return Response({"error": "Vendedor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateVendedorSerilizer(vendedor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Esta api es para eliminar un vendedor
@api_view(['DELETE'])
def delete_vendedor(request, id):
    try:
        vendedor = models.vendedor.objects.get(id_vendedor=id)
    except models.vendedor.DoesNotExist:
        return Response({"error": "Vendedor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    vendedor.delete()
    return Response({"mensaje": "Vendedor eliminado correctamente."}, status=status.HTTP_200_OK)