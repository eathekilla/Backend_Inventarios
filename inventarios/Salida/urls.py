from django.urls import path
from .views import SalidaListCreateView, SalidaRetrieveUpdateDeleteView,SalidaCreateAPIView,SalidaEntradaAPIView,SalidaReverseAPIView

urlpatterns = [
    path('list/', SalidaListCreateView.as_view(), name='salida-list-create'),
    path('retrieve/<int:pk>/', SalidaRetrieveUpdateDeleteView.as_view(), name='salida-retrieve-update-delete'),
    path('crearsalida/',SalidaCreateAPIView.as_view(),name='salida-retretive'),
    path('createsalida/',SalidaEntradaAPIView.as_view(),name='salida_api'),
    path('reverse/<int:pk>/', SalidaReverseAPIView.as_view(), name='salida-reverse'),
]
