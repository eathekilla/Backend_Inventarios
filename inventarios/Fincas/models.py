from django.db import models
from django.contrib.auth.models import User

class Finca(models.Model):
    codigo = models.CharField(max_length=150, null=True)
    nombre_finca = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150, null=True)
    telefono = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.nombre_finca}"

class Lotes(models.Model):
    nombre_lote = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150, null=True, default="")
    hectareas = models.FloatField(default=0)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, related_name='lotes',null=True)

    def __str__(self):
        return f"{self.nombre_lote}"

class Bodegas(models.Model):
    codigo = models.CharField(max_length=5, null=True, default="")
    nombre_bodega = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150, null=True, default="")
    lote = models.ForeignKey(Lotes, on_delete=models.CASCADE, related_name='bodegas',null=True)
    usuario = models.ManyToManyField(User, null=True, related_name='bodegas_finca_usuario')

    def __str__(self):
        return f"{self.nombre_bodega}"

class InfoUser(models.Model):
    telefono = models.CharField(max_length=12)
    direccion = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=20)
    usuario = models.ForeignKey(User,related_name="info_user",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario}"


def arbol(user):
    # Obtener todas las fincas
    lotes = Lotes.objects.filter(bodegas__usuario=user)
    fincas = Finca.objects.filter(lotes__in=lotes).prefetch_related('lotes', 'lotes__bodegas') 


    # Crear una lista para almacenar la estructura anidada
    estructura = []

    for finca in fincas:
        # Crear un diccionario para la finca actual
        finca_dict = {
            'id':finca.id,
            'nombre_finca': finca.nombre_finca,
            'ubicacion': 'finca.ubicacion',
            'telefono': finca.telefono,
            'lotes': []  # Lista para los lotes de esta finca
        }
        
        # Iterar sobre los lotes de la finca actual
        for lote in finca.lotes.all():
            lote_dict = {
                'id': lote.id,
                'nombre_lote': lote.nombre_lote,
                'ubicacion': 'lote.ubicacion',
                'hectareas': lote.hectareas,
                'bodegas': [{'id':bodega.id,'nombre_bodega': bodega.nombre_bodega, 'ubicacion': 'bodega.ubicacion'} for bodega in lote.bodegas.all()]  # Lista de diccionarios para bodegas
            }
            
            # Añadir el diccionario del lote a la lista de lotes de la finca
            finca_dict['lotes'].append(lote_dict)
        
        # Añadir la estructura de la finca a la lista principal
        estructura.append(finca_dict)
    return estructura

# Define la función de prueba para verificar si el usuario es específico o superusuario


