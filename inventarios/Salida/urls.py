from django.urls import path
from .views import SalidaListCreateView, SalidaRetrieveUpdateDeleteView,SalidaCreateView,SalidaCreateAPIView

urlpatterns = [
    path('list/', SalidaListCreateView.as_view(), name='salida-list-create'),
    path('create/', SalidaCreateView.as_view(), name='salida-create'),
    path('retrieve/<int:pk>/', SalidaRetrieveUpdateDeleteView.as_view(), name='salida-retrieve-update-delete'),
    path('crearsalida/',SalidaCreateAPIView.as_view(),name='salida-retretive')
]
