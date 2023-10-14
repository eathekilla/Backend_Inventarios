from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from Fincas.models import InfoUser
from Proveedor.models import Proveedor
from Insumo.models import Insumo,IngredienteActivo,Certificacion,Grupo,UnidadMedida
from Entrada.models import Entrada
from Salida.models import Salida
from Fincas.models import Bodegas,Lotes,Finca, arbol



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

def add_proveedor(request,prov_id=None):
    if prov_id:
        prov_instance = get_object_or_404(Proveedor,id=prov_id)
        return render(request,"html/app/add-proveedor.html",{'providerId': prov_instance.pk})
    else:
        return render(request,"html/app/add-proveedor.html")

def list_proveedor(request):
    return render(request,"html/app/list-proveedor.html") 


def add_insumo(request,insumo_id=None):
    unidades_medida = UnidadMedida.objects.all()
    certificaciones = Certificacion.objects.all()
    context ={
        "unidades_medida":unidades_medida,
        "certificaciones":certificaciones
    }
    if insumo_id:
        insumo_instance = get_object_or_404(Insumo,id=insumo_id)
        context["insumoId"] = insumo_instance.pk
        return render(request,"html/app/add-insumo.html",context)
    else:
        return render(request,"html/app/add-insumo.html",context)
    
def list_insumo(request):
    insumo_instance = Insumo.objects.all()
    return render(request,"html/app/list-insumos.html",{"insumos":insumo_instance})

def add_certificacion(request,cert_id=None):
    if cert_id:
        cert_instance = get_object_or_404(Certificacion,pk=cert_id)
        return render(request,"html/app/add-certificacion.html",{'cert_id': cert_instance.pk})
    else:
        return render(request,"html/app/add-certificacion.html")
    
def list_certificacion(request):
    return render(request,"html/app/list-certificacion.html")

def add_ingrediente(request,ingrediente_id=None):
    
    if ingrediente_id:
        insumo_instance = get_object_or_404(IngredienteActivo,pk=ingrediente_id)
        return render(request,"html/app/add-ingrediente.html",{'ingrediente_id': insumo_instance.pk})
    else:
        return render(request,"html/app/add-ingrediente.html")
    
def list_ingrediente(request):
    return render(request,"html/app/list-ingrediente.html")

def add_grupo(request):
    return render(request,"html/app/add-grupos.html")
def list_grupo(request):
    return render(request,"html/app/list-grupos.html")


def add_unidad(request,unidad_id=None):
    if unidad_id:
        insumo_instance = get_object_or_404(UnidadMedida,pk=unidad_id)
        return render(request,"html/app/add-unidad.html",{'unidad_id': insumo_instance.pk})
    else:
        return render(request,"html/app/add-unidad.html")
    
def list_unidad(request):
    return render(request,"html/app/list-unidad.html")


def add_entradas(request,entradas_id=None):
    unidades = UnidadMedida.objects.all()
    estructura = arbol()
    proveedores = Proveedor.objects.all()
    insumos = Insumo.objects.all()

    if entradas_id:
        entradas_instance = get_object_or_404(Entrada,pk=entradas_id)
        entradas_instance.unidad_id = entradas_instance.insumo.unidad_medida.id
        entradas_instance.proveedor_id = entradas_instance.proveedor.id
        
        bodega_preseleccionada = entradas_instance.bodega.pk
        bodega_instance = get_object_or_404(Bodegas,pk=bodega_preseleccionada)
        lote_preseleccionado = bodega_instance.lote
        finca_preseleccionada = lote_preseleccionado.finca
        


        context = {
            'entradas_id': entradas_instance.pk,
            'entradas':entradas_instance,
            'unidades_medida':unidades,
            'estructura': estructura,
            'proveedores':proveedores,
            'bodega_preseleccionada':bodega_preseleccionada,
            'lote_preseleccionado':lote_preseleccionado.pk,
            'finca_preseleccionada':finca_preseleccionada.pk,
            'insumo_preseleccionado':entradas_instance.insumo.pk,
            'insumos':insumos
            }
        return render(request,"html/app/add-entradas.html",context)
    else:
        return render(request,"html/app/add-entradas.html",{"insumos":insumos,"unidades_medida":unidades,'estructura': estructura,'proveedores':proveedores})
    
def list_entradas(request):
    entradas_instance = Entrada.objects.all()
    for entrada in entradas_instance:
        entrada.total = entrada.valor_unitario_entrada_a * entrada.cantidad
        entrada.unidad_medida = entrada.insumo.unidad_medida
    return render(request,"html/app/list-entradas.html",{'entradas':entradas_instance})

def list_entradas_primer_status(request):
    historial = Entrada.history.all().order_by('history_date')
    unidades = UnidadMedida.objects.all()
    # Crear un diccionario para almacenar el primer registro de cada grupo por el campo identificador (ID)
    primeros_registros = {}
    for entrada in historial:
        identificador = entrada.identificador
        if identificador not in primeros_registros:
            primeros_registros[identificador] = entrada

    # Ordenar los registros por fecha de historial en orden ascendente
    historial_ordenado = sorted(primeros_registros.values(), key=lambda entrada: entrada.history_date)
    context = {'unidades_medida':unidades,'entradas':historial_ordenado}
    return render(request,"html/app/list-entradas-inicial.html",context)

def list_fincas(request):
    fincas = Finca.objects.all()
    return render(request,"html/app/list-fincas.html",{'fincas':fincas})

def add_fincas(request,fincas_id=None):
    if fincas_id:
        fincas_instance = get_object_or_404(Finca,pk=fincas_id)
        return render(request,"html/app/add-fincas.html",{'fincas_id': fincas_instance.pk,'finca':fincas_instance})
    else:
        return render(request,"html/app/add-fincas.html")


def list_lotes(request):
    lotes = Lotes.objects.all()
    return render(request,"html/app/list-lotes.html",{'lotes':lotes})


def add_lotes(request,lotes_id=None):
    fincas = Finca.objects.all()
    estructura = arbol()
    context = {'fincas':fincas,'estructura':estructura}

    if lotes_id:
        lotes_instance = get_object_or_404(Lotes,pk=lotes_id)
        context["lotes_id"] = lotes_instance.pk
        context["lote_edit"] = lotes_instance
        context["finca_preseleccionada"] = lotes_instance.finca.pk

    return render(request,"html/app/add-lotes.html",context)


def list_bodegas(request):
    bodegas = Bodegas.objects.all()
    return render(request,"html/app/list-bodegas.html",{'bodegas':bodegas})

def add_bodegas(request,bodegas_id=None):
    bodegas = Bodegas.objects.all()
    usuarios = User.objects.all()
    estructura = arbol()
    context = {'bodegas':bodegas,'estructura': estructura,'usuarios':usuarios}

    if bodegas_id:
        bodega_instance = get_object_or_404(Bodegas,pk=bodegas_id)
        context["bodegas_id"] = bodega_instance.pk
        context["bodega_edit"] = bodega_instance
        context["lote_preseleccionado"] = bodega_instance.lote.pk
        context["finca_preseleccionada"] = bodega_instance.lote.finca.pk
        context["usuarios_preseleccionados"] = list(bodega_instance.usuario.all().values_list('pk',flat=True))
        

    return render(request,"html/app/add-bodegas.html",context)


def list_salidas(request):
    salidas_instance = Salida.objects.all()
    return render(request,"html/app/list-salidas.html",{'salidas':salidas_instance})

def add_salidas(request, salidas_id=None):
    insumos = Insumo.objects.all()
    bodegas = Bodegas.objects.all()
    context = {
        "insumos":insumos,
        "bodegas":bodegas
    }


    return render(request,"html/app/add-salidas.html",context)
