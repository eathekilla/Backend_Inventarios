from django.urls import path
from .views import EntradaListCreateView, EntradaRetrieveUpdateDeleteView

urlpatterns = [
    path('list-create/', EntradaListCreateView.as_view(), name='entrada-list-create'),
    path('retrieve/<int:pk>/', EntradaRetrieveUpdateDeleteView.as_view(), name='entrada-retrieve-update-delete'),
]
