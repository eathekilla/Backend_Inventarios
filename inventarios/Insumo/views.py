from rest_framework import generics
from .models import IngredienteActivo, Certificacion, UnidadMedida, Insumo, Grupo
from .serializers import IngredienteActivoSerializer, CertificacionSerializer, UnidadMedidaSerializer, InsumoSerializer, GrupoSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Sum,Avg
from Entrada.models import Entrada
from Insumo.models import Insumo
import json
from django.db.models.functions import Coalesce

class IngredienteActivoListCreateView(generics.ListCreateAPIView):
    queryset = IngredienteActivo.objects.all()
    serializer_class = IngredienteActivoSerializer

class IngredienteActivoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngredienteActivo.objects.all()
    serializer_class = IngredienteActivoSerializer

class CertificacionListCreateView(generics.ListCreateAPIView):
    queryset = Certificacion.objects.all()
    serializer_class = CertificacionSerializer

class CertificacionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificacion.objects.all()
    serializer_class = CertificacionSerializer

class UnidadMedidaListCreateView(generics.ListCreateAPIView):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer

class UnidadMedidaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer

class InsumoListCreateView(generics.ListCreateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def perform_create(self, serializer):
        insumo = serializer.save()
        grupo_id = self.request.data.get('grupo')
        if grupo_id:
            grupo = Grupo.objects.get(pk=grupo_id)
            grupo.insumos.add(insumo)
            grupo.save()

class InsumoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def perform_update(self, serializer):
        insumo = serializer.save()
        grupo_id = self.request.data.get('grupo')
        if grupo_id:
            # Eliminar todos los grupos asociados al insumo
            insumo.grupos.clear()
            grupo = Grupo.objects.get(pk=grupo_id)
            grupo.insumos.add(insumo)
            grupo.save()
class GrupoListCreateView(generics.ListCreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class GrupoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

@api_view(['GET'])
def consultar_insumos_grupo(request, grupo_id):
    try:
        grupo = Grupo.objects.get(pk=grupo_id)
        insumos = grupo.insumos.all()
        
        insumos_data = [{"id": insumo.id, "nombre": insumo.nombre} for insumo in insumos]
        
        return JsonResponse({"success": True, "insumos": insumos_data})
    except Grupo.DoesNotExist:
        return JsonResponse({"success": False, "message": "Grupo no encontrado"})

@api_view(['GET','PUT'])
def edit_info_proveedor(request, pk):
    try:
        insumo =  get_object_or_404(Insumo,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    '''if request.method == 'PUT':
        serializer = EditeUserWithInfoUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
    
    if request.method == 'GET':
        insumo =  get_object_or_404(Insumo,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        grupo = Grupo.objects.filter(insumos=insumo).first()
        proveedor_data = {
                    "id": insumo.pk,
                    "nombre": insumo.nombre,
                    "codigo_contable": insumo.codigo_contable,
                    "unidad_medida": insumo.unidad_medida.pk,
                    "certificacion": insumo.certificacion.pk,
                    "ingrediente": insumo.ingrediente.pk,
                    "carencia": insumo.carencia,
                    "grupo": grupo.pk if grupo else None
                    }
    
        return Response(proveedor_data, status=status.HTTP_200_OK)
    return Response({"message": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET','PUT'])
def edit_ingrediente(request, pk):
    try:
        ingrediente =  get_object_or_404(IngredienteActivo,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = IngredienteActivoSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        ingrediente =  get_object_or_404(IngredienteActivo,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        ingrediente_data = {
                    "id": ingrediente.pk,
                    "nombre": ingrediente.nombre,
                    }
        return Response(ingrediente_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Ingrediente no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT'])
def edit_certificacion(request, pk):
    try:
        certificacion =  get_object_or_404(Certificacion,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = CertificacionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        certificacion =  get_object_or_404(Certificacion,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        certificacion_data={    "periodo_reingreso": certificacion.periodo_reingreso,
                                "registro_ica": certificacion.registro_ica,
                                "fecha_registro": certificacion.fecha_registro,
                            }
        return Response(certificacion_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Certificacion no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT'])
def edit_unidad(request, pk):
    try:
        unidad =  get_object_or_404(UnidadMedida,pk=pk)
    except Insumo.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UnidadMedidaSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        unidad =  get_object_or_404(UnidadMedida,pk=pk)  # Obtén los grupos a los que pertenece el usuario
        unidad_data = {
                    "id": unidad.pk,
                    "nombre": unidad.nombre,
                    }
        return Response(unidad_data, content_type='application/json', status=status.HTTP_200_OK)
    return Response({"message": "Ingrediente no encontrado"}, status=status.HTTP_404_NOT_FOUND)




def cantidad_total_insumo(request, id_insumo):
    insumo = get_object_or_404(Insumo,id=id_insumo)
    unidad_medida = insumo.unidad_medida
    return JsonResponse({'unidad_medida': unidad_medida.nombre})



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse
from datetime import datetime, timedelta

def alerta_proximas_a_vencer(request):
    # Configuración de Gmail
    gmail_user = 'inventarioscrecento@gmail.com'
    gmail_password = 'monidblpfeuzfwga'

    # Calcula la fecha de hoy y la fecha límite para las entradas a vencer
    today = datetime.now()
    one_week_later = today + timedelta(weeks=1)

    # Consulta las entradas que vencen en una semana
    entradas_a_vencer = Entrada.objects.filter(fecha_vencimiento__gte=today, fecha_vencimiento__lte=one_week_later)

    # Configuración del correo
    subject = f'Alerta: Entradas próximas a vencer - {today.strftime("%Y-%m-%d")}'
    from_email = gmail_user
    recipient_list = ['inventarioscrecento@gmail.com']  # Reemplaza con la dirección del destinatario

    # Cuerpo del correo
    message = 'Las siguientes entradas vencerán en una semana:\n\n'
    for entrada in entradas_a_vencer:
        message += f"Entrada: {entrada.insumo}\n"
        message += f"Bodega: {entrada.bodega}\n"
        message += f"Lote: {entrada.bodega.lote}\n"
        message += f"Finca: {entrada.bodega.lote.finca}\n"
        message += f"Cantidad: {entrada.cantidad}\n"
        message += f"Proveedor: {entrada.proveedor}\n"
        message += f"Identificador: {entrada.identificador}\n"
        message += f"Fecha de vencimiento: {entrada.fecha_vencimiento}\n"
        message += '--------------------------------------\n'

    try:
        # Configura el servidor SMTP de Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)

        # Crea el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Envía el correo
        server.sendmail(from_email, recipient_list, msg.as_string())
        server.close()

        return HttpResponse('Correo de alerta enviado exitosamente.')
    except Exception as e:
        return HttpResponse(f'Error al enviar el correo: {str(e)}')


def enviar_correo_prueba(request):
    # Configuración de Gmail
    gmail_user = 'inventarioscrecento@gmail.com'
    gmail_password = 'monidblpfeuzfwga'  # Reemplaza con tu contraseña de Gmail

    # Configuración del correo
    subject = 'Prueba de envío de correo desde Django'
    from_email = gmail_user
    recipient_list = ['eamezquita97@gmail.com']  # Reemplaza con tu dirección de correo

    # Cuerpo del correo
    message = 'Este es un correo de prueba enviado desde Django.'

    try:
        # Configura el servidor SMTP de Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)

        # Crea el mensaje
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Envía el correo
        server.sendmail(from_email, recipient_list, msg.as_string())
        server.close()

        print('Correo de prueba enviado exitosamente.')
    except Exception as e:
        print(f'Error al enviar el correo de prueba: {str(e)}')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Insumo
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

@method_decorator(csrf_exempt, name='dispatch')  # Añade este decorador si necesitas desactivar la protección CSRF
class InsumoListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):

        if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
            return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)
        
        insumos = Insumo.objects.all()
        insumo_list = []

        for insumo in insumos:
            #valor_unitario_prom =  Entrada.objects.filter(insumo=insumo).aggregate(Avg('valor_unitario_entrada_a'))
            # Suponiendo que insumo es el objeto de insumo que estás buscando

            # Intenta obtener la entrada asociada al insumo
            entrada = Entrada.objects.filter(insumo=insumo).first()

            # Si no hay entrada asociada, establece el valor promedio en cero
            if not entrada:
                valor_unitario_prom = 0
            else:
                # Calcula el valor promedio de las unidades de entrada
                valor_unitario_prom_qery = Entrada.objects.filter(insumo=insumo).aggregate(Avg('valor_unitario_entrada_a'))
                valor_unitario_prom = valor_unitario_prom_qery['valor_unitario_entrada_a__avg']

            # Ahora valor_unitario_prom contendrá el promedio de valor_unitario_entrada_a si hay entradas asociadas al insumo,
            # de lo contrario, contendrá cero.
            grupo = Grupo.objects.filter(insumos=insumo).first()
            if grupo:
                grupo_nombre = grupo.nombre
            else:
                grupo_nombre = "Sin Grupo"
            insumo_data = {
                'nombre': insumo.nombre,
                'codigo_contable': insumo.codigo_contable,
                'unidad_medida': insumo.unidad_medida.unidad if insumo.unidad_medida else None,
                'valor_unitario_prom': round(valor_unitario_prom, 2),
                'grupo':grupo_nombre
            }
            insumo_list.append(insumo_data)

        return JsonResponse({'insumos': insumo_list}, safe=False)
