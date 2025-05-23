# Generated by Django 4.2.7 on 2025-05-05 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('schedules', '0001_initial'),
        ('barbers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmada'), ('completed', 'Completada'), ('cancelled', 'Cancelada')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='barbers.barberprofile')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='schedules.timeslot')),
            ],
        ),
    ]
