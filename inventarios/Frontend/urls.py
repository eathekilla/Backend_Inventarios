
from django.urls import path
from .views import *

urlpatterns = [
    path('', test_view, name='home'),
    path('login/',login, name='login'),

    path('add-user/', add_user, name='add_user'),
    path('list-users/', list_users, name='list_users'),
    path('user/edit/<int:user_id>/', add_user, name='edit_user'),

    path('add-proveedor/', add_proveedor, name='add_proveedor'),
    path('list-proveedor/', list_proveedor, name='list_proveedor'),

    path('add-insumo/', add_insumo, name='add_insumo'),
    path('list-insumo/', list_insumo, name='list_insumo'),

    path('add-certificacion/', add_certificacion, name='add_certificacion'),
    path('list-certificacion/', list_certificacion, name='list_certificacion'),

    path('add-ingrediente/', add_ingrediente, name='add_ingrediente'),
    path('list-ingrediente/', list_ingrediente, name='list_ingrediente'),

    path('add-grupo/', add_grupo, name='add_grupo'),
    path('list-grupo/', list_grupo, name='list_grupo'),

    
    
]