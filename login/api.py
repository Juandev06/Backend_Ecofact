from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from users.models import user
from . import serializes



class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        try:
            # primero generamos los tokens usando el metodo padre que es el super de la clase TokenObtainPairView que hace la generacion de los tokens para usarlos desdes postman en el bearer token
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refress_token = tokens['refresh']

            # necesitamos obtener el usuario autenticado para asignarselo a la cookie
            user = authenticate(
                username=request.data['username'],
                password=request.data['password']
            )

            if not user:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            # si el usuario es valido entonces procedemos a crear las cookies
            response = Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
            # validamos si el ususario esta activo en la base de datos
            if not user.is_active:
                return Response({"error": "Usuario inactivo"}, status=status.HTTP_403_FORBIDDEN)
            ## respuesta con los tokens creados ##

            res = Response()
            res.data = { # devolvemos en la data los tokens creados y el rol del usuario para que al momento de logearse se pueda redirigir a la pagina correspondiente 
                'access':access_token,
                'refress':refress_token,
                'role': user.rol,
            }

            # configuramos las cookies
            res.set_cookie(
                key='access_token', # Key es el nombre de la cookie
                value=access_token, # value es el valor de la cookie
                httponly=True, # httponly es para que la cookie no pueda ser accedida por javascript
                secure=True, # secure es para que la cookie solo se envie por https
                samesite='None', # samesite es para que la cookie pueda ser enviada en solicitudes de terceros
                path='/', # path es para que la cookie sea enviada en todas las rutas del dominio
            )
# set cookie es un metodo que recibe varios parametros para configurar la cookie de tal manera que pueda generar la cookie #
            res.set_cookie(
                key='refresh_token',
                value=refress_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )

            return res
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenRefreshObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token') # obtenemos el refresh token de la cookie
            request.data['refresh'] = refresh_token # asignamos el refresh token a la data del request para que pueda ser usado por el metodo padre eso quiere decir que el metodo padre va a usar el refresh token que esta en la cookie para generar un nuevo token de acceso
            response = super().post(request, *args, **kwargs) # llamamos al metodo padre de la clase TokenObtainPairView para generar los tokens
            tokens = response.data # obtenemos los tokens generados y los almacenamos en la variable tokens
            access_token = tokens['access'] # obtenemos el token de acceso
            res = Response() # creamos una respuesta vacia

            res.data = { # creamos un diccionario con los mensajes de exito cuando se renueva el token
                'refresed': 'Token de acceso renovado exitosamente',
            } 
            # aqui creamos la cookie cuando se hace el refresh token con el nuevo token de acceso 
            res.set_cookie(
                key='access_token', # Key es el nombre de la cookie
                value=access_token, 
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )

            return res
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Aqui vamos a empezar a implementar la logica del logeo de los usuarios###


# El siguiente metodo es el login del Admin, que se va a logear con correo y contraseña y se va a autenticar que el rol del usuario sea Admin para que pueda ingresar a la plataforma de administracion #
@api_view(['POST'])
def login_admin(request):
        serializer = serializes.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.rol == 'Admin':
                return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
            return Response({'error': 'Credenciales inválidas o usuario no es admin'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# El siguente metodo es el login del vendedor, que se logueará con correo y contraseña y se auteticará con el rol venedor para acceder a la plataforma de ventas #
@api_view(['POST'])
def login_vendedor(request):
        serializer = serializes.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.rol == 'Vendedor':
                return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
            return Response({'error': 'Credenciales inválidas o usuario no es vendedor'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# El siguente metodo es el login del cliente, que se logueará con correo y contraseña y se auteticará con el rol cliente para acceder a la plataforma de clientes #
@api_view(['POST'])
def login_cliente(request):
        serializer = serializes.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.rol == 'Cliente':
                return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
            return Response({'error': 'Credenciales inválidas o usuario no es cliente'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


