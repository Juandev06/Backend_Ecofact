from . import models
from rest_framework.serializers import ModelSerializer 

##-------------------------------------------------------------------------------------------------------------------##
class GetUsersSerializer(ModelSerializer):
    class Meta:
        model = models.user # Esta forma se conoce como encapsulamiento y es una buena práctica para mantener el código organizado y fácil de mantener.
        fields = ['id', 'username', 'email', 'rol']
        # read_only_fields = ['id', 'username', 'email']

    def list_user(self):
        return self.Meta.model.objects.all() # el metodo all() devuelve todos los objetos de la clase cliente consultando a la base de datos

####-----------------------Empezamos la creacion de los metodos para crear usuarios---------------####


## El funcionamiento del formato JSON es clave:valor ##
class ClienteSerializer(ModelSerializer): # creamos una clase serializadora para el modelo cliente para serializar todos los campos del modelo y usarla mas adelante en los serializadores que se van a crear
    class Meta:
        model = models.cliente
        fields = '__all__' # los field son todos los campos del modelo que se van a serializar
        # la serializacion es el proceso de convertir un objeto en un formato que se pueda almacenar o transmitir y luego reconstruirlo. que en este caso es convertir el objeto en un formato JSON para enviarlo a través de una API
        read_only_fields = ['id_cliente', 'user'] # los campos que no se pueden modificar, en este caso el id_cliente y el user que es el usuario al que pertenece el cliente


## esta clase es la que va a crear los usuarios clientes y va a recibir los datos del cliente para crear el cliente asociado al usuario
class UserCreateSerializer(ModelSerializer):
    cliente = ClienteSerializer(source='Cliente',required=True) # asignamos a una variable la clase serializada de cliente para recibir los datos del cliente y usarlos en el metodo create

    class Meta: # la clase Meta es una clase interna que se usa para configurar el comportamiento del serializer prinicipalmente para definir el modelo y los campos que se van a serializar
        model = models.user # tomamos el modelo user del archivo models.py
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} # el write_only es para que no se vea la contraseña al momento de serializar el objeto
    
    def create(self, validated_data): # el metodo create es el que se encarga de crear un nuevo objeto en la base de datos a partir de los datos validados que recibe el serializer
        cliente_data = validated_data.pop('Cliente', None)# el .pop es para sacar el cliente del diccionario
        # el metdod validated_data es un diccionario que contiene los datos que han sido validados por el serializer y estos datos vienen del request.data que se recibe en la vista el ''cliente'' es el nombre del campo que definimos en la clase UserCreateSerializer
        user = models.user.objects.create_user(**validated_data) # el ** es oara desempaquetar el diccionario y pasar mas de un argumento a la vez al metodo create_user que es un metodo que viene por defecto en el modelo user y se encarga de crear un nuevo usuario en la base de datos 
        if user.rol == 'Cliente' and cliente_data: # si el rol del usuario es cliente y si hay datos del cliente
            models.cliente.objects.create(user=user, **cliente_data)  # creamos el cliente y le asignamos el usuario que acabamos de crear y los datos del cliente que vienen del diccionario cliente_data
        return user # y retornamos el objeto user que es el usuario que acabamos de crear


# Este serializer es para obtener los datos del cliente
class GetClientesSerializer(ModelSerializer):
    class Meta:
        model = models.cliente
        fields = [
            'id_cliente', 'user', 'nombre_cliente', 'apellido_cliente',
            'tipo_documento', 'numero_documento', 'direccion_cliente',
            'telefono_cliente', 'correo_cliente', 'fecha_creacion'
        ]
        read_only_fields = ['id_cliente', 'user']
##-------------------------------------------------------------------------------------------------------------------##

# Este serializer es para actualizar los datos del cliente

class UpdateClienteSerializer(ModelSerializer):
    class Meta:
        model = models.cliente
        fields = ['nombre_cliente', 'apellido_cliente', 'direccion_cliente', 'telefono_cliente']
        read_only_fields = ['id_cliente', 'user']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


##-------------------------------------------------------------------------------------------------------------------## 


# Este serializer es para actualizar los datos del usuario
class EmpresaAdminSerializer(ModelSerializer):
    class Meta:
        model = models.empresaAdmin
        fields = '__all__'
        read_only_fields = ['id_empresa', 'user']

# Este serializer es para crear un nuevo administrador de empresa
class EmpresaAdminCreateSerializer( ModelSerializer):
    empresaAdmin = EmpresaAdminSerializer(required=True)# este es el que va a recibir los datos del admin

    class Meta:
        model = models.user
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        empresa_data = validated_data.pop('empresaAdmin', None)
        user = models.user.objects.create_user(**validated_data)
        if user.rol == 'Admin' and empresa_data:
            models.empresaAdmin.objects.create(user=user, **empresa_data)
        return user


class GetAdminSerializer(ModelSerializer): # creamos una clase serializadora para obtener los administradores de empresa
    class Meta:
        model = models.empresaAdmin
        fields = [
            'id_empresa', 'user', 'nit_empresa', 'nombre_empresa',
            'direccion_empresa', 'telefono_empresa', 'correo_empresa',
            'representante_legal', 'cufe'
        ]
        read_only_fields = ['id_empresa', 'user']

    def list_admin(self):
        admins = self.Meta.model.objects.all()
        return admins
        
# Este serializer es para eliminar un administrador de empresa
class DeleteAdminSerializer(ModelSerializer):
    class Meta:
        model = models.user
        fields = ['id', 'username', 'email']  # Campos básicos, no empresa (ya quitamos empresa)
        read_only_fields = ['id', 'username', 'email']

    def delete_admin(self, id):
        try:
            admin = self.Meta.model.objects.get(id=id, rol="Admin")
            admin.delete()
            return admin
        except self.Meta.model.DoesNotExist:
            return None

##-------------------------------------------------------------------------------------------------------------------##

## En el siguiente bloque de codigo se van a crear los serializadores para los vendedores ##
##-------------------------------------------------------------------------------------------------------------------##

class VendedorSerializer(ModelSerializer): # creamos una clase serializadora para el modelo vendedor para serializar todos los campos del modelo y usarla mas adelante en los serializadores que se van a crear
    class Meta:
        model = models.vendedor
        fields = '__all__'
        read_only_fields = ['id_vendedor', 'user']
        
        
        
        
class CreateVendedorSerializer(ModelSerializer): # creamos una clase serializadora para crear un nuevo vendedor y va a recibir los datos del vendedor para crear el vendedor asociado al usuario
    vendedor = VendedorSerializer(write_only=True, required=True)

    class Meta:
        model = models.user
        fields = ['username', 'password', 'rol', 'vendedor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        vendedor_data = validated_data.pop('vendedor', None)
        user = models.user.objects.create_user(**validated_data)
        if user.rol == 'Vendedor' and vendedor_data:
            models.vendedor.objects.create(user=user, **vendedor_data)
        return user


# creamos una clase serializadora para obtener los vendedores
class GetVendedoreSerializer(ModelSerializer):
    class Meta:
        model = models.vendedor
        fields = ['id_vendedor', 'user', 'nombre_vendedor', 'apellido_vendedor', 'telefono_vendedor']
        read_only_fields = ['id_vendedor', 'user']



# Serializer para listar todos los vendedores
class GetVendedoresSerializer(ModelSerializer): 
    class Meta:
        model = models.vendedor
        fields = [
            'id_vendedor', 'user', 'nombre_vendedor', 'apellido_vendedor',
            'tipo_documento', 'numero_documento', 'direccion_vendedor',
            'telefono_vendedor', 'correo_vendedor'
        ]
        read_only_fields = ['id_vendedor', 'user']



# Serializer para actualizar un vendedor
class UpdateVendedorSerilizer(ModelSerializer):
    class Meta:
        model = models.vendedor
        fields = ['nombre_vendedor', 'apellido_vendedor', 'direccion_vendedor', 'telefono_vendedor', 'correo_vendedor']
        read_only_fields = ['id_vendedor', 'user']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    
    
    
# Serializer para eliminar un vendedor
class DeleteVendedorSerializer(ModelSerializer):
    class Meta:
        model = models.user
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']

    def delete_vendedor(self, id):
        try:
            vendedor = self.Meta.model.objects.get(id=id, rol="Vendedor")
            vendedor.delete()
            return vendedor
        except self.Meta.model.DoesNotExist:
            return None    
