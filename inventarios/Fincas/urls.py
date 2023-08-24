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
	path('fincauser/',views.FincaList.as_view(),name='fincaslist')
]