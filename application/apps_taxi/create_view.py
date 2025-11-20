"""
Script to create the core_turno_serviciosrview database view.
Run this from the Django project directory.
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ['DJANGO_READ_DOT_ENV_FILE'] = 'True'
django.setup()

from django.db import connection

# SQL to create the view
sql = """
CREATE OR REPLACE VIEW core_turno_serviciosrview AS
SELECT
    fecha_programacion AS fecha,
    SUM(llamadas_atendidos) AS llamadas_atendidas,
    SUM(servicios_registradas) AS registrados,
    SUM(servicios_asignadas) AS asignados
FROM core_turno_turnooperador
GROUP BY fecha_programacion
ORDER BY fecha_programacion DESC;
"""

print("Creating database view core_turno_serviciosrview...")
try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    print("SUCCESS: View created successfully!")
except Exception as e:
    print(f"ERROR: {e}")
