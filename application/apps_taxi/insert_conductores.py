"""
Script to insert test conductores (drivers) into the database.
Run this from the Django shell or as a standalone script.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.core_conductor.models import Conductor
from apps.core_conductor.constants import CONDUCTOR_ESTADO_DISPONIBLE

# Conductores (drivers) test data
conductores_data = [
    {
        "nombre": "Juan",
        "apellido_paterno": "Pérez",
        "apellido_materno": "García",
        "estado": CONDUCTOR_ESTADO_DISPONIBLE,
        "direccion": "Calle Principal 123",
        "telefono": "555-0101",
        "licencia": "LIC123456",
        "clase": "A",
        "created_by": "admin",
        "modified_by": "admin",
    },
    {
        "nombre": "María",
        "apellido_paterno": "López",
        "apellido_materno": "Martínez",
        "estado": CONDUCTOR_ESTADO_DISPONIBLE,
        "direccion": "Avenida Central 456",
        "telefono": "555-0102",
        "licencia": "LIC789012",
        "clase": "B",
        "created_by": "admin",
        "modified_by": "admin",
    },
    {
        "nombre": "Carlos",
        "apellido_paterno": "González",
        "apellido_materno": "Rodríguez",
        "estado": CONDUCTOR_ESTADO_DISPONIBLE,
        "direccion": "Boulevard Norte 789",
        "telefono": "555-0103",
        "licencia": "LIC345678",
        "clase": "A",
        "created_by": "admin",
        "modified_by": "admin",
    },
]

# Insert conductores
print("Inserting conductores (drivers)...")
for conductor_data in conductores_data:
    # Check if conductor already exists by name
    exists = Conductor.objects.filter(
        nombre=conductor_data["nombre"],
        apellido_paterno=conductor_data["apellido_paterno"]
    ).exists()

    if not exists:
        # Create new conductor (cod_conductor will be auto-generated)
        conductor = Conductor.objects.create(**conductor_data)
        print(f"✓ Created: {conductor.cod_conductor} - {conductor.nombre} {conductor.apellido_paterno}")
    else:
        print(f"  Already exists: {conductor_data['nombre']} {conductor_data['apellido_paterno']}")

# Check total
total = Conductor.objects.filter(estado__in=["01", "02", "03", "04"]).count()
print(f"\nTotal active conductores: {total}")

if total > 0:
    print("\nActive conductores:")
    for c in Conductor.objects.filter(estado__in=["01", "02", "03", "04"]).order_by('cod_conductor'):
        print(f"  - {c.cod_conductor}: {c.nombre} {c.apellido_paterno} (Estado: {c.get_estado_display()}, Licencia: {c.licencia})")
else:
    print("\nWARNING: No active conductores found!")

print("\nDone!")
