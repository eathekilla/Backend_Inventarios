from django.urls import path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
	path('register/', views.UserRegister.as_view(), name='register'),
	path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('logout/', views.UserLogout.as_view(), name='logout'),
	path('user/', views.UserView.as_view(), name='user'),
    path('fincas/', views.FincaView.as_view(), name='fincas'),
	path('fincauser/',views.FincaList.as_view(),name='fincaslist'),
    path('lotes/list-create/',views.LotesListCreateView.as_view(),name='lotes-list-create'),
    path('lotes/retrieve/<int:pk>/',views.LotesRetrieveUpdateDeleteView.as_view(), name='lotes-retretive'),
    path('bodegas/list-create/',views.BodegasListCreateView.as_view(),name='bodegas-list-create'),
    path('bodegas/retrieve/<int:pk>/',views.BodegasRetrieveUpdateDeleteView.as_view(), name='bodegas-retretive'),
    path('finca/list-create/',views.FincaListCreateView.as_view(),name='fincas-list-create'),
    path('finca/list-tree/',views.FincaRelListCreateView.as_view(),name='fincas-list-create'),
	path('finca/retrieve/<int:pk>/',views.FincaRetrieveUpdateDeleteView.as_view(), name='fincas-retretive'),
    path('info/create/', views.create_user_with_info_user, name='userinfo'),
    path('info/edit/<int:pk>/', views.edit_info_user, name='edit-info-user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('info/all/', views.get_all_info_users, name='userinfo'),
    
]