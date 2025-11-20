# Generated migration to add validators to dia_semana field
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_maestras", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grupohorariodetalle",
            name="dia_semana",
            field=models.SmallIntegerField(
                choices=[
                    (1, "Lunes"),
                    (2, "Martes"),
                    (3, "Miércoles"),
                    (4, "Jueves"),
                    (5, "Viernes"),
                    (6, "Sábado"),
                    (7, "Domingo"),
                ],
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(7),
                ],
                verbose_name="Dia de la semana",
            ),
        ),
    ]
