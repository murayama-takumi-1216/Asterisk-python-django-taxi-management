# Estado de los turnos (conductor/operador)
ESTADO_TURNO_PENDIENTE = "01"  # <-- usar
ESTADO_TURNO_PROGRAMADO = "02"  # <-- usar
ESTADO_TURNO_ACTIVO = "03"  # <-- usar
ESTADO_TURNO_CONCLUIDO = "04"  # <-- usar
ESTADO_TURNO_CANCELADO = "05"
ESTADO_TURNO_REPROGRAMADO = "06"

ESTADO_TURNO_CHOICES = (
    (ESTADO_TURNO_PENDIENTE, "Pendiente"),
    (ESTADO_TURNO_PROGRAMADO, "Programado"),
    (ESTADO_TURNO_ACTIVO, "En proceso"),
    (ESTADO_TURNO_CONCLUIDO, "Concluido"),
    (ESTADO_TURNO_CANCELADO, "Cancelado"),
    (ESTADO_TURNO_REPROGRAMADO, "Reprogramado"),
)
