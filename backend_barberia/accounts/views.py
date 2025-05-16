# accounts/views.py
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from barbers.models import BarberProfile, Specialty, BarberSpecialty
from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy', 'me']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'me']:
            return UserProfileSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin(request):
    """Verifica si el usuario autenticado es administrador"""
    is_admin = request.user.is_staff
    return Response({'isAdmin': is_admin})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_barber(request):
    """Registra un nuevo usuario y crea su perfil de barbero"""
    try:
        # Validar datos del usuario
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number', '')
        
        if not all([username, email, password, first_name, last_name]):
            return Response(
                {"error": "Todos los campos de usuario son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "El nombre de usuario ya está en uso"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo electrónico ya está en uso"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        
        # Datos del perfil de barbero
        bio = request.data.get('bio', '')
        years_of_experience = request.data.get('years_of_experience', 0)
        instagram_profile = request.data.get('instagram_profile', '')
        
        # Crear el perfil de barbero
        barber = BarberProfile.objects.create(
            user=user,
            bio=bio,
            years_of_experience=years_of_experience,
            instagram_profile=instagram_profile
        )
        
        # Asignar especialidades si se proporcionan
        specialties = request.data.get('specialties', [])
        for specialty_id in specialties:
            try:
                specialty = Specialty.objects.get(id=specialty_id)
                BarberSpecialty.objects.create(
                    barber=barber,
                    specialty=specialty
                )
            except Specialty.DoesNotExist:
                pass  # Ignorar especialidades que no existen
        
        return Response(
            {"message": "Barbero registrado exitosamente"},
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        # Si ocurre un error, eliminar el usuario si ya fue creado
        if 'user' in locals():
            user.delete()
            
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )