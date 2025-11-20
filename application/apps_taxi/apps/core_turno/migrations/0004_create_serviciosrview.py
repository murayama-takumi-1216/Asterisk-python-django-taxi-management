# Generated migration to create database view
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core_turno", "0003_serviciosdiaview"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE VIEW core_turno_serviciosrview AS
            SELECT
                fecha_programacion AS fecha,
                SUM(llamadas_atendidos) AS llamadas_atendidas,
                SUM(servicios_registradas) AS registrados,
                SUM(servicios_asignadas) AS asignados
            FROM core_turno_turnooperador
            GROUP BY fecha_programacion
            ORDER BY fecha_programacion DESC;
            """,
            reverse_sql="""
            DROP VIEW IF EXISTS core_turno_serviciosrview;
            """,
        ),
    ]
