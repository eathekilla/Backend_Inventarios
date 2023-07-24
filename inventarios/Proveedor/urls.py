from django.urls import path
from .views import ProveedorListCreateView, ProveedorRetrieveUpdateDeleteView

urlpatterns = [
    path('list-create/', ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('retrieve/<int:pk>/', ProveedorRetrieveUpdateDeleteView.as_view(), name='proveedor-retrieve-update-delete'),
]
