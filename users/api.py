from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializer
from . import models
from rest_framework import status


#Este endpoint recibe datos, los valida con el serializer, crea un usuario en la base de datos y responde con los datos del nuevo usuario o con errores si algo está mal.
@api_view(['POST'])
def create_user(request):
    user_serializer = serializer.UserCreateSerializer(data=request.data)
    if user_serializer.is_valid():
        if user_serializer.validated_data.get('rol') == 'Cliente':
            user = user_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "El rol debe ser 'cliente' para crear un cliente."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Este endpoint acepta solo peticiones GET y devuelve una lista de los usuarios en la base de datos.
@api_view(['GET'])
def get_users(request):
    users = serializer.GetUsersSerializer()
    return Response(users.data, status=status.HTTP_200_OK) 

##----------------------------------------------------------------------------------------------------##
@api_view(['PUT'])
def update_user(reques):
    user = serializer.UpdateUserSerializer(data=reques.data)
    if user.is_valid():
        user = user.save()
        return Response(status=status.HTTP_200_OK)
    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
##----------------------------------------------------------------------------------------------------##
# Ejemplo de JSON para crear un nuevo cliente
# {
#   "username": "juan",
#   "password": "1234",
#   "rol": "Cliente",
#   "cliente": {
#     "nombre_cliente": "Juan",
#     "apellido_cliente": "Pérez",
#     "tipo_documento": "CC",
#     "numero_documento": "12345678",
#     "direccion_cliente": "Calle 123",
#     "telefono_cliente": "3001234567",
#     "correo_cliente": "juan@email.com"
#   }
# }

#Este endpoint recibe datos, los valida con el serializer, crea un administrador de empresa en la base de datos y responde con los datos del nuevo administrador o con errores si algo está mal.
@api_view(['POST'])
def create_empresa_admin(request):
    empresa_admin_serializer = serializer.EmpresaAdminCreateSerializer(data=request.data)
    if empresa_admin_serializer.is_valid():
        if empresa_admin_serializer.validated_data.get('rol') == 'Admin':
            empresa_admin_serializer = empresa_admin_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "El rol debe ser 'Admin' para crear un administrador de empresa."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(empresa_admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
##----------------------------------------------------------------------------------------------------##

#Este endpoint devuelve una lista de todos los administradores de empresa en la base de datos.

@api_view(['GET'])
def list_admins(request):
    admin_serializer = serializer.getadminSerializer(many=True)
    return Response(admin_serializer.data, status=status.HTTP_200_OK)


#Este endpoint elimina un administrador de empresa por su ID.
@api_view(['DELETE'])
def delete_admin(request, id):
    try:
        admin = models.user.objects.get(id=id, rol="Admin")  # Filtramos que realmente sea un Admin
    except models.user.DoesNotExist:
        return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    admin.delete()
    return Response({"mensaje": "Administrador eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)




# Este endpoint recibe un ID de cliente en la URL, verifica que el cliente exista y lo elimina de la base de datos.
@api_view(['DELETE'])
def delete_cliente(request, id):
    try:
        cliente = models.user.objects.get(id=id, rol="Cliente")  # Filtramos que realmente sea un Cliente
    except models.user.DoesNotExist:
        return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    cliente.delete()
    return Response({"mensaje": "Cliente eliminado correctamente."}, status=status.HTTP_200_OK)

# Ejemplo de JSON para crear un nuevo administrador de empresa
#{
# "username": "nuevoadministrador",
#"password": "1234admin",
#"rol": "Admin",
#"empresaAdmin": {
# "nombre_empresa": "Nueva Empresa S.A.S.",
    #"nit_empresa": "900987654",
    #"direccion_empresa": "Carrera 45 #67-89",
    #"telefono_empresa": "3209876543",
    #"correo_empresa": "contacto@nuevaempresa.com",
    #"regimen_empresa": "comun",
    #"representante_legal": "Carlos Pérez",
    #"cufe": "CUFE987654"
#}
#}

##----------------------------------------------------------------------------------------------------##
# Se va a empezar a crear los endpoints para los vendedores
##----------------------------------------------------------------------------------------------------##
