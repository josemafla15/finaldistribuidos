# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register_barber, check_admin
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt

# Crea el router
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Rutas relacionadas con el viewset de UserViewSet
    path('', include(router.urls)),

    # Ruta para obtener el token de autenticación
    path('auth/token/', csrf_exempt(obtain_auth_token)),
    
    # Nuevas rutas
    path('register-barber/', register_barber, name='register_barber'),
    path('check-admin/', check_admin, name='check_admin'),
]