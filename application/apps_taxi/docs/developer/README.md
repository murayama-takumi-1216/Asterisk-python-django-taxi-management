# Taxi Developer

# generar loaddata

```shell
python -Xutf8 manage.py dumpdata --indent=2 auth.group > apps/users/fixtures/groups.json
python -Xutf8 manage.py dumpdata --indent=2 users.user > apps/users/fixtures/user.json
python -Xutf8 manage.py dumpdata --indent=2 core_maestras.horario > apps/core_maestras/fixtures/horario.json
python -Xutf8 manage.py dumpdata --indent=2 core_vehiculo.vehiculo > apps/core_vehiculo/fixtures/vehiculo.json
python -Xutf8 manage.py dumpdata --indent=2 core_conductor.conductor > apps/core_conductor/fixtures/conductor.json
python -Xutf8 manage.py dumpdata --indent=2 core_operador.operador > apps/core_operador/fixtures/operador.json


```
