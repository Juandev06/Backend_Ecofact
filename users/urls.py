from django.urls import path
from . import api

urlpatterns = [
    #Estas rutas las precede el path 'api/' que está en el archivo ecofact/urls.py
    
    # Usuarios
    
    path('create-user/',api.create_user, name='create_user'),
    path('update-user/', api.update_user, name='update_user'),
    path('users/', api.get_users, name='get_users'),
    
    # Clientes
    
    path('list-clientes/', api.list_clientes, name='list_clientes'),
    path('update-cliente/<str:id>/', api.update_cliente, name='update_cliente'),
    path('delete-cliente/<str:id>/', api.delete_cliente, name='delete_cliente'),

    # Admins

    path('create-empresa-admin/', api.create_empresa_admin, name='create_empresa_admin'),
    path('list-admins/', api.list_admins, name='list_admins'),
    path('delete-admin/<int:id>/', api.delete_admin, name='delete_admin'),

    # Vendedores  
    
    path('create-vendedor/', api.create_vendedor, name='create_vendedor'),
    path('list-vendedores/', api.list_vendedores, name='list_vendedores'),
    path('get-vendedor/<str:id>/', api.get_vendedor, name='get_vendedor'),
    path('update-vendedor/<str:id>/', api.update_vendedor, name='update_vendedor'),
    path('delete-vendedor/<str:id>/', api.delete_vendedor, name='delete_vendedor'),

]