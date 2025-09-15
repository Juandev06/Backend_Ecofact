from django.urls import path
from . import api

urlpatterns = [
    #Estas rutas las precede el path 'api/' que está en el archivo ecofact/urls.py
    path('create-user/',api.create_user, name='create_user'),
    path('users/', api.get_users, name='get_users'),
    path('create-empresa-admin/', api.create_empresa_admin, name='create_empresa_admin'),
    path('list-admins/', api.list_admins, name='list_admins'),
    path('delete-admin/<int:id>/', api.delete_admin, name='delete_admin'),
    path('update-user/', api.update_user, name='update_user'),
    path('delete-cliente/<int:id>/', api.delete_cliente, name='delete_cliente'),
    
]