from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from Fincas.models import InfoUser


def test_view(request):
    return render(request,"html/app/todo.html")

def login(request):
    return render(request,'html/app/auth-sign-in.html')


def add_user(request,user_id=None):
    if user_id:
        user_instance = get_object_or_404(User, id=user_id)
        return render(request,"html/app/add-usuario.html",{'userId': user_instance.pk})
        
    else:
        return render(request,"html/app/add-usuario.html")
    
def list_users(request):
    return render(request,"html/app/list-usuarios.html") 

def add_proveedor(request):
    return render(request,"html/app/add-proveedor.html")

def list_proveedor(request):
    return render(request,"html/app/list-proveedor.html") 


def add_insumo(request):
    return render(request,"html/app/add-insumo.html")
def list_insumo(request):
    return render(request,"html/app/list-insumos.html")

def add_certificacion(request):
    return render(request,"html/app/add-certificacion.html")
def list_certificacion(request):
    return render(request,"html/app/list-certificacion.html")

def add_ingrediente(request):
    return render(request,"html/app/add-ingrediente.html")
def list_ingrediente(request):
    return render(request,"html/app/list-ingrediente.html")

def add_grupo(request):
    return render(request,"html/app/add-grupos.html")
def list_grupo(request):
    return render(request,"html/app/list-grupos.html")