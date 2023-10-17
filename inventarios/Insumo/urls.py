from django.urls import path
from .views import (
    IngredienteActivoListCreateView, IngredienteActivoRetrieveUpdateDeleteView,
    CertificacionListCreateView, CertificacionRetrieveUpdateDeleteView,
    UnidadMedidaListCreateView, UnidadMedidaRetrieveUpdateDeleteView,
    InsumoListCreateView, InsumoRetrieveUpdateDeleteView,cantidad_total_insumo,
    GrupoListCreateView, GrupoRetrieveUpdateDeleteView,edit_info_proveedor,edit_ingrediente,edit_certificacion,edit_unidad, consultar_insumos_grupo
)

urlpatterns = [
    path('ingredientes-activos/list-create/', IngredienteActivoListCreateView.as_view(), name='ingrediente-activo-list-create'),
    path('ingredientes-activos/retrieve/<int:pk>/', IngredienteActivoRetrieveUpdateDeleteView.as_view(), name='ingrediente-activo-retrieve-update-delete'),
    path('certificaciones/list-create/', CertificacionListCreateView.as_view(), name='certificacion-list-create'),
    path('certificaciones/retrieve/<int:pk>/', CertificacionRetrieveUpdateDeleteView.as_view(), name='certificacion-retrieve-update-delete'),
    path('unidades-medida/list-create/', UnidadMedidaListCreateView.as_view(), name='unidad-medida-list-create'),
    path('unidades-medida/retrieve/<int:pk>/', UnidadMedidaRetrieveUpdateDeleteView.as_view(), name='unidad-medida-retrieve-update-delete'),
    path('list-create/', InsumoListCreateView.as_view(), name='insumo-list-create'),
    path('retrieve/<int:pk>/', InsumoRetrieveUpdateDeleteView.as_view(), name='insumo-retrieve-update-delete'),
    path('grupos/list-create/', GrupoListCreateView.as_view(), name='grupo-list-create'),
    path('grupos/retrieve/<int:pk>/', GrupoRetrieveUpdateDeleteView.as_view(), name='grupo-retrieve-update-delete'),
    path('editar/<int:pk>/',edit_info_proveedor,name="editar_get_insumo"),
    path('editar/ingrediente/<int:pk>/',edit_ingrediente,name="editar_get_ingrediente"),
    path('editar/certificacion/<int:pk>/',edit_certificacion,name="editar_get_certificacion"),
    path('editar/unidad/<int:pk>/',edit_unidad,name="editar_get_unidad"),
    path('cantidad-total/<int:id_insumo>/', cantidad_total_insumo, name='cantidad_total_insumo'),
    path('consultar_grupo/<int:grupo_id>/', consultar_insumos_grupo, name='consultar_grupo'),

    
]
