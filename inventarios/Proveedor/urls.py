from django.urls import path
from .views import ProveedorListCreateView, ProveedorRetrieveUpdateDeleteView, edit_info_proveedor

urlpatterns = [
    path('list-create/', ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('retrieve/<int:pk>/', ProveedorRetrieveUpdateDeleteView.as_view(), name='proveedor-retrieve-update-delete'),
    path('edit/<int:pk>/',edit_info_proveedor,name='edit_get_provider')
]
