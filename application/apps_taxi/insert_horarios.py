"""
Script to insert horarios into the database.
Run this from the Django shell or as a standalone script.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.core_maestras.models import Horario

# Horarios data
horarios_data = [
    {
        "cod_horario": "01",
        "nom_horario": "Madrugada",
        "inicio_horario": "00:00:00",
        "fin_horario": "08:00:00",
        "orden_view": 1,
        "estado": True,
        "horario_base": True,
        "created_by": "admin",
        "modified_by": "admin",
    },
    {
        "cod_horario": "02",
        "nom_horario": "Mañana",
        "inicio_horario": "08:00:00",
        "fin_horario": "16:00:00",
        "orden_view": 2,
        "estado": True,
        "horario_base": True,
        "created_by": "admin",
        "modified_by": "admin",
    },
    {
        "cod_horario": "03",
        "nom_horario": "Tarde",
        "inicio_horario": "16:00:00",
        "fin_horario": "00:00:00",
        "orden_view": 3,
        "estado": True,
        "horario_base": True,
        "created_by": "admin",
        "modified_by": "admin",
    },
]

# Insert horarios
print("Inserting horarios...")
for horario_data in horarios_data:
    horario, created = Horario.objects.get_or_create(
        cod_horario=horario_data["cod_horario"],
        defaults=horario_data
    )
    if created:
        print(f"✓ Created: {horario.cod_horario} - {horario.nom_horario}")
    else:
        print(f"  Already exists: {horario.cod_horario} - {horario.nom_horario}")

# Check total
total = Horario.objects.filter(estado=True).count()
print(f"\nTotal active horarios: {total}")

if total > 0:
    print("\nActive horarios:")
    for h in Horario.objects.filter(estado=True).order_by('orden_view'):
        print(f"  - {h.cod_horario}: {h.nom_horario} ({h.inicio_horario} - {h.fin_horario})")
else:
    print("\nWARNING: No active horarios found!")

print("\nDone!")
