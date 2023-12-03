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
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Suponiendo que "nombre_de_tu_vista" es el nombre de la URL de la vista a la que quieres redirigir
            return redirect(reverse('list_entradas'))
        else:
            # Aquí puedes agregar un mensaje de error si lo deseas
            context = {"error": "Credenciales incorrectas"}
            return render(request, 'html/app/auth-sign-in.html', context)
    else:
        return render(request, 'html/app/auth-sign-in.html')

def logout_view(request):
    auth_logout(request)
    return redirect(reverse('login'))

@login_required
def test_view(request):
    return render(request, "html/app/todo.html")

@login_required
def add_user(request,user_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if user_id:
        user_instance = get_object_or_404(User, id=user_id)
        return render(request,"html/app/add-usuario.html",{'userId': user_instance.pk,'token':token,'grupos_usuario': grupos_usuario})
        
    else:
        return render(request,"html/app/add-usuario.html",{'token':token})

@login_required    
def list_users(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"token":token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-usuarios.html",context) 
@login_required
def add_proveedor(request,prov_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if prov_id:
        prov_instance = get_object_or_404(Proveedor,id=prov_id)
        return render(request,"html/app/add-proveedor.html",{'providerId': prov_instance.pk,'token':token,'grupos_usuario': grupos_usuario})
    else:
        return render(request,"html/app/add-proveedor.html",{'token':token,'grupos_usuario': grupos_usuario})
@login_required
def list_proveedor(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    proveedores = Proveedor.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))

    return render(request,"html/app/list-proveedor.html",{'token':token,'proveedores':proveedores,'user':user,'grupos_usuario': grupos_usuario}) 

@login_required
def add_insumo(request,insumo_id=None):
    unidades_medida = UnidadMedida.objects.all()
    certificaciones = Certificacion.objects.all()
    ingredientes = IngredienteActivo.objects.all()
    grupo_insumos = Grupo.objects.all()
    user = get_object_or_404(User,email=request.user.email)
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    token = str(AccessToken.for_user(user))
    context ={
        "unidades_medida":unidades_medida,
        "certificaciones":certificaciones
        ,'token':token
        ,"grupos":grupo_insumos
        ,'grupos_usuario': grupos_usuario,
        'ingredientes':ingredientes,
    }
    if insumo_id:
        insumo_instance = get_object_or_404(Insumo,id=insumo_id)
        if insumo_instance.certificacion:
            context['certificacion'] = insumo_instance.certificacion.pk
        if insumo_instance.ingrediente:
            context['ingrediente'] = insumo_instance.ingrediente.pk
        if insumo_instance.unidad_medida:
            context['unidad_medida'] = insumo_instance.unidad_medida.pk
        if insumo_instance.grupos:
            context['grupos'] = list(insumo_instance.grupos.values_list('pk',flat=True))
        context["insumoId"] = insumo_instance.pk
        return render(request,"html/app/add-insumo.html",context)
    else:
        return render(request,"html/app/add-insumo.html",context)

@login_required   
def list_insumo(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    insumo_instance = Insumo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-insumos.html",{"insumos":insumo_instance,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_certificacion(request,cert_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    ingredientes = IngredienteActivo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"ingredientes":ingredientes,'token':token,'grupos_usuario': grupos_usuario}

    if cert_id:
        cert_instance = get_object_or_404(Certificacion,pk=cert_id)
        context['cert_id'] = cert_instance.pk
        return render(request,"html/app/add-certificacion.html",context)
    else:
        return render(request,"html/app/add-certificacion.html",context)
@login_required
def add_certificacion_insumo(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    ingredientes = IngredienteActivo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"ingredientes":ingredientes,'token':token,'grupos_usuario': grupos_usuario}
    

    return render(request,"html/app/add-certificacion-insumo.html",context)


@login_required
def list_certificacion(request):
    certificaciones = Certificacion.objects.all()
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    
    return render(request,"html/app/list-certificacion.html",{'certificaciones':certificaciones,'token':token,'grupos_usuario': grupos_usuario})


@login_required
def add_ingrediente(request,ingrediente_id=None):
    ingredientes = IngredienteActivo.objects.all()
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'ingredientes': ingredientes,'token':token,'grupos_usuario': grupos_usuario}
    if ingrediente_id:
        insumo_instance = get_object_or_404(IngredienteActivo,pk=ingrediente_id)
        context['ingrediente_id'] = insumo_instance.pk
        context['insumo_instance'] = insumo_instance
        return render(request,"html/app/add-ingrediente.html",context)
    else:
        return render(request,"html/app/add-ingrediente.html",context)

@login_required
def add_ingrediente_insumo(request):
    ingredientes = IngredienteActivo.objects.all()

    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'ingredientes': ingredientes,'token':token,'grupos_usuario': grupos_usuario}
    return render(request, 'html/app/add-ingrediente-insumo.html',context)

@login_required
def list_ingrediente(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    ingredientes = IngredienteActivo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'ingredientes': ingredientes,'token':token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-ingrediente.html",context)


@login_required
def add_grupo(request,grupo_id=None):
    insumos = Insumo.objects.all()
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"insumos":insumos,'token':token,'grupos_usuario': grupos_usuario}
    
    if grupo_id:
        grupo_instance = get_object_or_404(Grupo,pk=grupo_id)
        context['grupo_id'] = grupo_instance.pk
        context['grupo_instance'] = grupo_instance
        context['insumos_grupo'] = list(grupo_instance.insumos.values_list("id",flat=True))
        return render(request,"html/app/add-grupos.html",context)
    return render(request,"html/app/add-grupos.html",context)


@login_required
def add_grupo_insumo(request,grupo_id=None):
    insumos = Insumo.objects.all()
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"insumos":insumos,'token':token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/add-grupos-insumos.html",context)

@login_required
def list_grupo(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos = Grupo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"grupos":grupos,'token':token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-grupos.html",context)

@login_required
def add_unidad(request,unidad_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if unidad_id:
        insumo_instance = get_object_or_404(UnidadMedida,pk=unidad_id)
        return render(request,"html/app/add-unidad.html",{'unidad_id': insumo_instance.pk,'token':token,'grupos_usuario': grupos_usuario})
    else:
        return render(request,"html/app/add-unidad.html",{'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_unidad_insumo(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/add-unidad-insumo.html",{'token':token,'grupos_usuario': grupos_usuario})


@login_required
def list_unidad(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    unidades = UnidadMedida.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {"unidades":unidades,'token':token,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-unidad.html",context)

@login_required
def add_entradas(request,entradas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    unidades = UnidadMedida.objects.all()
    estructura = arbol()
    proveedores = Proveedor.objects.all()
    insumos = Insumo.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))

    if entradas_id:
        entradas_instance = get_object_or_404(Entrada,pk=entradas_id)
        entradas_instance.unidad_id = entradas_instance.insumo.unidad_medida.id
        entradas_instance.proveedor_id = entradas_instance.proveedor.id
        
        if entradas_instance.bodega:
            bodega_preseleccionada = entradas_instance.bodega.pk
            bodega_instance = get_object_or_404(Bodegas,pk=bodega_preseleccionada)
            lote_preseleccionado = bodega_instance.lote.pk
            finca_preseleccionada = bodega_instance.lote.finca.pk
        else:
            bodega_preseleccionada = ""
            lote_preseleccionado = ""
            finca_preseleccionada = ""
        


        context = {
            'entradas_id': entradas_instance.pk,
            'entradas':entradas_instance,
            'unidades_medida':unidades,
            'estructura': estructura,
            'proveedores':proveedores,
            'bodega_preseleccionada':bodega_preseleccionada,
            'lote_preseleccionado':lote_preseleccionado,
            'finca_preseleccionada':finca_preseleccionada,
            'insumo_preseleccionado':entradas_instance.insumo.pk,
            'insumos':insumos
            ,'token':token
            ,'grupos_usuario': grupos_usuario
            }
        return render(request,"html/app/add-entradas.html",context)
    else:
        return render(request,"html/app/add-entradas.html",{"insumos":insumos,"unidades_medida":unidades,'estructura': estructura,'proveedores':proveedores,'token':token})

@login_required    
def list_entradas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    entradas_instance = Entrada.objects.filter(cantidad__gt=0).order_by('fecha_creacion')
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    for entrada in entradas_instance:
        entrada.total = entrada.valor_unitario_entrada_a * entrada.cantidad
        entrada.unidad_medida = entrada.insumo.unidad_medida
    return render(request,"html/app/list-entradas.html",{'entradas':entradas_instance,'token':token,'grupos_usuario': grupos_usuario})


@login_required
def list_entradas_primer_status(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    historial = Entrada.history.all().order_by('history_date')
    unidades = UnidadMedida.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    # Crear un diccionario para almacenar el primer registro de cada grupo por el campo identificador (ID)
    primeros_registros = {}
    for entrada in historial:
        identificador = entrada.identificador
        entrada.total = entrada.valor_unitario_entrada_a * entrada.cantidad
        user = get_object_or_404(User,email=request.user.email)
        #entrada.unidad_medida = entrada.insumo.unidad_medida
        if identificador not in primeros_registros:
            primeros_registros[identificador] = entrada

    # Ordenar los registros por fecha de historial en orden ascendente
    historial_ordenado = sorted(primeros_registros.values(), key=lambda entrada: entrada.history_date)
    context = {'unidades_medida':unidades,'entradas':historial_ordenado,'grupos_usuario': grupos_usuario}
    return render(request,"html/app/list-entradas-inicial.html",context)


@login_required
def list_fincas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    fincas = Finca.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-fincas.html",{'fincas':fincas,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_fincas(request,fincas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    if fincas_id:
        fincas_instance = get_object_or_404(Finca,pk=fincas_id)
        return render(request,"html/app/add-fincas.html",{'fincas_id': fincas_instance.pk,'finca':fincas_instance,'token':token,'grupos_usuario': grupos_usuario})
    else:
        return render(request,"html/app/add-fincas.html",{'token':token,'grupos_usuario': grupos_usuario})

@login_required
def list_lotes(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    lotes = Lotes.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-lotes.html",{'lotes':lotes,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_lotes(request,lotes_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    fincas = Finca.objects.all()
    estructura = arbol()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'fincas':fincas,'estructura':estructura,'token':token,'grupos_usuario': grupos_usuario}

    if lotes_id:
        lotes_instance = get_object_or_404(Lotes,pk=lotes_id)
        context["lotes_id"] = lotes_instance.pk
        context["lote_edit"] = lotes_instance
        context["finca_preseleccionada"] = lotes_instance.finca.pk

    return render(request,"html/app/add-lotes.html",context)

@login_required
def list_bodegas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    bodegas = Bodegas.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-bodegas.html",{'bodegas':bodegas,'token':token,'grupos_usuario': grupos_usuario})

@login_required
def add_bodegas(request,bodegas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    bodegas = Bodegas.objects.all()
    usuarios = User.objects.all()
    estructura = arbol()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {'bodegas':bodegas,'estructura': estructura,'usuarios':usuarios,'token':token,'grupos_usuario': grupos_usuario}

    if bodegas_id:
        bodega_instance = get_object_or_404(Bodegas,pk=bodegas_id)
        context["bodegas_id"] = bodega_instance.pk
        context["bodega_edit"] = bodega_instance
        context["lote_preseleccionado"] = bodega_instance.lote.pk
        context["finca_preseleccionada"] = bodega_instance.lote.finca.pk
        context["usuarios_preseleccionados"] = list(bodega_instance.usuario.all().values_list('pk',flat=True))
        

    return render(request,"html/app/add-bodegas.html",context)

@login_required
def list_salidas(request):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    salidas_instance = Salida.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return render(request,"html/app/list-salidas.html",{'salidas':salidas_instance,'token':token,'grupos_usuario': grupos_usuario})
@login_required
def add_salidas(request, salidas_id=None):
    user = get_object_or_404(User,email=request.user.email)
    token = str(AccessToken.for_user(user))
    insumos = Insumo.objects.all()
    bodegas = Bodegas.objects.all()
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    context = {
        "insumos":insumos,
        "bodegas":bodegas
        ,'token':token
        ,'grupos_usuario': grupos_usuario
    }


    return render(request,"html/app/add-salidas.html",context)
