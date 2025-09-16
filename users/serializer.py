from . import models
from rest_framework.serializers import ModelSerializer as serializer



##-------------------------------------------------------------------------------------------------------------------##
class GetUsersSerializer(serializer):
    class Meta:
        model = models.cliente # Esta forma se conoce como encapsulamiento y es una buena práctica para mantener el código organizado y fácil de mantener.
        fields = ['id', 'username', 'email', 'first_name']
        # read_only_fields = ['id', 'username', 'email']

    def list_user(self):
        return self.Meta.model.objects.all() # el metodo all() devuelve todos los objetos de la clase cliente consultando a la base de datos
##-------------------------------------------------------------------------------------------------------------------##



####-----------------------Empezamos la creacion de los metodos para crear usuarios---------------####

##-------------------------------------------------------------------------------------------------------------------##

## el funcionamiento del formato JSON es clave:valor ##
class ClienteSerializer(serializer):
    class Meta:
        model = models.cliente
        fields = '__all__' # los field son todos los campos del modelo que se van a serializar
        # la serializacion es el proceso de convertir un objeto en un formato que se pueda almacenar o transmitir y luego reconstruirlo. que en este caso es convertir el objeto en un formato JSON para enviarlo a través de una API
        read_only_fields = ['id_cliente', 'user'] # los campos que no se pueden modificar, en este caso el id_cliente y el user que es el usuario al que pertenece el cliente


## esta clase es la que va a crear los usuarios clientes y va a recibir los datos del cliente para crear el cliente asociado al usuario
class UserCreateSerializer(serializer):
    cliente = ClienteSerializer(required=True) # asignamos a una variable la clase serializada de cliente para recibir los datos del cliente y usarlos en el metodo create

    class Meta: # la clase Meta es una clase interna que se usa para configurar el comportamiento del serializer prinicipalmente para definir el modelo y los campos que se van a serializar
        model = models.user # tomamos el modelo user del archivo models.py
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} # el write_only es para que no se vea la contraseña al momento de serializar el objeto
    
    def create(self, validated_data): # el metodo create es el que se encarga de crear un nuevo objeto en la base de datos a partir de los datos validados que recibe el serializer
        cliente_data = validated_data.pop('cliente', None)# el .pop es para sacar el cliente del diccionario
        # el metdod validated_data es un diccionario que contiene los datos que han sido validados por el serializer y estos datos vienen del request.data que se recibe en la vista el ''cliente'' es el nombre del campo que definimos en la clase UserCreateSerializer
        user = models.user.objects.create_user(**validated_data) # el ** es oara desempaquetar el diccionario y pasar mas de un argumento a la vez al metodo create_user que es un metodo que viene por defecto en el modelo user y se encarga de crear un nuevo usuario en la base de datos 
        if user.rol == 'Cliente' and cliente_data: # si el rol del usuario es cliente y si hay datos del cliente
            models.cliente.objects.create(user=user, **cliente_data)  # creamos el cliente y le asignamos el usuario que acabamos de crear y los datos del cliente que vienen del diccionario cliente_data
        return user # y retornamos el objeto user que es el usuario que acabamos de crear



class GetClientesSerializer(serializer):
    class Meta:
        model = models.cliente
        fields = ['id_cliente', 'user', 'nombre', 'apellido', 'direccion', 'telefono']
        read_only_fields = ['id_cliente', 'user']
    def list_cliente(self):
        clientes = self.Meta.model.objects.all()
        return clientes
##-------------------------------------------------------------------------------------------------------------------##

# Este serializer es para actualizar los datos del cliente
class UpdateClienteSerializer(serializer):
    class Meta:
        model = models.cliente
        fields = ['nombre', 'apellido', 'direccion', 'telefono']
        read_only_fields = ['id_cliente', 'user']

        def update_cliente(self, id, validated_data): # el metodo update_cliente recibe el id del cliente que se va a actualizar y los datos validados que se van a actualizar
            try:
                cliente = self.Meta.model.objects.get(id=id)
                for field, value in validated_data.items():
                    setattr(cliente, field, value)# el metodo setattr es para asignar un valor a un atributo de un objeto de forma dinamica es decir, en lugar de escribir cliente.nombre = value, usamos setattr(cliente, 'nombre', value) es muy similar a como funciona el diccionario y a condiciones ternarias para realizar validacion y asignacion en una sola linea
        # desde el frontend la manera de enviar los datos es enviando solo los campos que se van a actualizar, por ejemplo si solo se va a actualizar el nombre y el telefono, el diccionario validated_data va a contener solo esos dos campos y sus valores 
        # JSON ejemplo:
        # { "nombre": "Juan", "telefono": "123456789" } y asi sucesivamente
                cliente.save() # guardamos los cambios en la base de datos
                return cliente  # retornamos el objeto cliente que es el cliente que acabamos de actualizar
            except self.Meta.model.DoesNotExist:
                return None

##-------------------------------------------------------------------------------------------------------------------## 



# Este serializer es para actualizar los datos del usuario
class EmpresaAdminSerializer(serializer):
    class Meta:
        model = models.empresaAdmin
        fields = '__all__'
        read_only_fields = ['id_empresa', 'user']

# Este serializer es para crear un nuevo administrador de empresa
class EmpresaAdminCreateSerializer(serializer):
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


class getadminSerializer(serializer):
    class Meta:
        model = models.empresaAdmin
        fields = ['id_empresa', 'user', 'nombre_empresa', 'direccion', 'telefono']
        read_only_fields = ['id_empresa', 'user']

    def list_admin(self):
        admins = self.Meta.model.objects.all()
        return admins
        
# Este serializer es para eliminar un administrador de empresa
class DeleteAdminSerializer(serializer):
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

class VendedorSerializer(serializer): # creamos una clase serializadora para el modelo vendedor para serializar todos los campos del modelo y usarla mas adelante en los serializadores que se van a crear
    class Meta:
        model = models.vendedor
        fields = '__all__'
        read_only_fields = ['id_vendedor', 'user']


class CreateVendedorSerializer(serializer): # creamos una clase serializadora para crear un nuevo vendedor
    vendedor = VendedorSerializer(required=True) # asignamos a una variable la clase serializada de vendedor para recibir los datos del vendedor y usarlos en el metodo create

    class Meta: # la clase Meta es una clase interna que se usa para configurar el comportamiento del serializer prinicipalmente para definir el modelo y los campos que se van a serializar
        model = models.user # tomamos el modelo user del archivo models.py
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} # el write_only es para que no se vea la contraseña al momento de serializar el objeto
    
    def create(self, validated_data): # el metodo create es el que se encarga de crear un nuevo objeto en la base de datos a partir de los datos validados que recibe el serializer
        vendedor_data = validated_data.pop('vendedor', None)# el .pop es para sacar el vendedor del diccionario
        # el metodo validated_data es un diccionario que contiene los datos que han sido validados por el serializer y estos datos vienen del request.data que se recibe en la vista el ''vendedor'' es el nombre del campo que definimos en la clase CreateVendedorSerializer
        user = models.user.objects.create_user(**validated_data) # el ** es oara desempaquetar el diccionario y pasar mas de un argumento a la vez al metodo create_user que es un metodo que viene por defecto en el modelo user y se encarga de crear un nuevo usuario en la base de datos 
        if user.rol == 'Vendedor' and vendedor_data: # si el rol del usuario es Vendedor y si hay datos del Vendedor
            models.vendedor.objects.create(user=user, **vendedor_data)  # creamos el cliente y le asignamos el usuario que acabamos de crear y los datos del cliente que vienen del diccionario vendedor_data
        return user # y retornamos el objeto user que es el usuario que acabamos de crear

# creamos una clase serializadora para obtener los vendedores
class GetVendedoreSerializer(serializer):
    class Meta:
        model = models.vendedor
        fields = ['id_vendedor', 'user', 'nombre_vendedor', 'apellido_vendedor', 'telefono_vendedor']
        read_only_fields = ['id_vendedor', 'user']

# Serializer para listar todos los vendedores
class GetVendedoresSerializer(serializer): 
    class Meta:
        model = models.vendedor
        fields = [
            'id_vendedor', 'user', 'nombre_vendedor', 'apellido_vendedor',
            'tipo_documento', 'numero_documento', 'direccion_vendedor',
            'telefono_vendedor', 'correo_vendedor'
        ]
        read_only_fields = ['id_vendedor', 'user']


# Este endpoint es para actualizar los datos del vendedor
class UpdateVendedorSerilizer(serializer):
    class Meta:
        model = models.vendedor
        fields = ['nombre_vendedor', 'apellido_vendedor','direccion_vendedor', 'telefono_vendedor','correo_vendedor'] # falta en los requerimientos funcionales definir si se van a poder actualizar todos los campos o solo algunos
        read_only_fields = ['id_vendedor', 'user'] 

        def update_vendedor(self, id, validated_data): # el metodo update_vendedor recibe el id del vendedor que se va a actualizar y los datos validados que se van a actualizar
            try:
                vendedor = self.Meta.model.objects.get(id=id)
                for field, value in validated_data.items():
                    setattr(vendedor, field, value)# el metodo setattr es para asignar un valor a un atributo de un objeto de forma dinamica es decir, en lugar de escribir vendedor.nombre = value, usamos setattr(vendedor, 'nombre', value) es muy similar a como funciona el diccionario y a condiciones ternarias para realizar validacion y asignacion en una sola linea
        # desde el frontend la manera de enviar los datos es enviando solo los campos que se van a actualizar, por ejemplo si solo se va a actualizar el nombre y el telefono, el diccionario validated_data va a contener solo esos dos campos y sus valores 
        # JSON ejemplo:
        # { "nombre": "Pedro", "telefono": "987654321" } y asi sucesivamente
                vendedor.save() # guardamos los cambios en la base de datos
                return vendedor  # retornamos el objeto vendedor que es el vendedor que acabamos de actualizar
            except self.Meta.model.DoesNotExist:
                return None



##Este serializer es para eliminar un vendedor
class DeleteVendedorSerializer(serializer):
    class Meta:
        model = models.user
        fields = ['id', 'username', 'email']  
        read_only_fields = ['id_vendedor', 'user']

    def delete_vendedor(self, id):
        try:
            vendedor = self.Meta.model.objects.get(id=id, rol="Vendedor")
            vendedor.delete()
            return vendedor
        except self.Meta.model.DoesNotExist:
            return None
##-------------------------------------------------------------------------------------------------------------------##
