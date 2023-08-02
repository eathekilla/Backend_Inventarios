from django.urls import path
from .views import EntradaListCreateView, EntradaRetrieveUpdateDeleteView, InventarioHistoricoView, InventarioEstadoActualView, EntradaHistoricoView,EntradaPrimerHistoricoView

urlpatterns = [
    path('list-create/', EntradaListCreateView.as_view(), name='entrada-list-create'),
    path('retrieve/<int:pk>/', EntradaRetrieveUpdateDeleteView.as_view(), name='entrada-retrieve-update-delete'),
    path('inventario/historico/<int:insumo_id>/', InventarioHistoricoView.as_view(), name='inventario-historico'),
    path('inventario/estado-actual/', InventarioEstadoActualView.as_view(), name='inventario-estado-actual'),
    path('inventario/historico/', EntradaHistoricoView.as_view(), name='entrada-historico'),
    path('inventario/inicialentrada/', EntradaPrimerHistoricoView.as_view(), name='entrada-historico'),
    
]
