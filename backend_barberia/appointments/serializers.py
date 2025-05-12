# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment
from accounts.serializers import UserSerializer
from barbers.serializers import BarberProfileSerializer
from services.serializers import ServiceSerializer
from schedules.serializers import TimeSlotSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    customer_details = UserSerializer(source='customer', read_only=True)
    barber_details = BarberProfileSerializer(source='barber', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    time_slot_details = TimeSlotSerializer(source='time_slot', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_details', 'barber', 'barber_details',
            'service', 'service_details', 'time_slot', 'time_slot_details',
            'date', 'status', 'created_at', 'updated_at', 'notes'
        ]
        read_only_fields = ['created_at', 'updated_at']