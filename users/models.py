import cuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta,datetime



#Aquí se van a empezar a crear los modelos para el proyecto formativo de Ecofact

class user (AbstractUser):
    roles = [
        ("Admin","Admin"),
        ("Vendedor","Vendedor"),
        ("Cliente","Cliente")
        ]
    rol = models.CharField(max_length=10, choices=roles)
        
    #Encripta la constraseña ingresada por el usuario 
    def set_password(self, raw_password):
        return super().set_password(raw_password)
            


class empresaAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Admin")
    id_empresa = models.CharField(primary_key=True, max_length=50, default=cuid.cuid)
    nombre_empresa = models.CharField(max_length=100)
    nit_empresa = models.CharField(max_length=20)
    direccion_empresa = models.CharField(max_length=200)
    telefono_empresa = models.CharField(max_length=15)
    correo_empresa = models.EmailField(max_length=100)
    regimen_empresa = models.CharField(max_length=50, default="comun")
    representante_legal = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cufe = models.CharField(max_length=253)
    token = models.CharField(max_length=255, blank=True, null=True)
    
    def crear_token(self):
        import secrets
        self.token = secrets.token_hex(32)
        self.save()
        return self.token
    
# Modelo de Producto
class producto(models.Model):
    CATEGORIA_PRODUCTO_CHOICES = [
        ('Celulares', 'Celular'),
        ('Auriculares', 'Auricular'),
        ('Cargadores', 'Cargador'),
    ]

    id_producto = models.AutoField(primary_key=True, unique=True)
    nombre_producto = models.CharField(max_length=100)
    categoria_producto = models.CharField(max_length=20, choices=CATEGORIA_PRODUCTO_CHOICES)
    modelo_producto = models.CharField(max_length=50)
    capacidad_producto = models.IntegerField()
    color_producto = models.CharField(max_length=20)
    descripcion_producto = models.TextField(max_length=254, blank=False)
    precio_producto = models.DecimalField(max_digits=15, decimal_places=2)
    codigo_barras_producto = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    
    
# Modelo de Inventario
class inventario(models.Model):
    id_inventario = models.CharField(primary_key=True, max_length=50, default=cuid.cuid)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)

# Modelo de Cliente
class cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Cliente")
    id_cliente = models.CharField(primary_key=True, max_length=50, default=cuid.cuid, unique=True)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    tipos_documento = [
        ("CC","Cedula de Ciudadania"),
        ("CE","Cedula de Extranjeria"),
        ("NIT","NIT"),
        ("PAS","Pasaporte")
    ]
    tipo_documento = models.CharField(choices=tipos_documento, default="CC", max_length=4)
    numero_documento = models.CharField(max_length=20)
    direccion_cliente = models.TextField(max_length=200)
    telefono_cliente = models.TextField(max_length=15)
    correo_cliente = models.EmailField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    
    def crear_token(self):
        import secrets
        self.token = secrets.token_hex(32)
        self.save()
        return self.token
        
    
# Modelo de Vendedor
class vendedor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Vendedor")
    id_vendedor = models.CharField(primary_key=True, max_length=50, default=cuid.cuid)
    nombre_vendedor = models.CharField(max_length=100)
    apellido_vendedor = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=4, default="CC")
    numero_documento = models.CharField(max_length=20)
    direccion_vendedor = models.TextField(max_length=200)
    telefono_vendedor = models.CharField(max_length=15)
    correo_vendedor = models.EmailField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    
    def crear_token(self):
        import secrets
        self.token = secrets.token_hex(32)
        self.save()
        return self.token
    
# Modelo de Factura
class factura(models.Model):
    id_factura = models.CharField(primary_key=True, max_length=50, default=cuid.cuid, unique=True)
    vendedor = models.ForeignKey(vendedor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(producto, through='DetalleFactura')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()
    total_sin_iva = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=4,decimal_places=2 , default=0.19)
    total_con_iva = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):## este metodo toma de la clase padre la fecha emision de la factura y la 
        #elimina 30 dias despues para realizar la fecha de vencimiento en caso de garantias de algun producto
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_emision + timedelta(days=30)
        self.total_con_iva = (self.total_sin_iva*self.iva) + self.total_sin_iva
        super().save(*args, **kwargs)
 
 
# Modelo de Detalle de Factura       
class DetalleFactura(models.Model):
    factura = models.ForeignKey(factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

# Modelo de Historial de Factura
class historialFactura(models.Model):
    id_historial = models.CharField(primary_key=True, max_length=50, default=cuid.cuid)
    factura = models.ForeignKey(factura, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    cambios_realizados = models.TextField()
    vendedor_responsable = models.ForeignKey(vendedor, on_delete=models.CASCADE)
