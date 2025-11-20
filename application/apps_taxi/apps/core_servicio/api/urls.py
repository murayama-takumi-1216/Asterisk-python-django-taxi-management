from rest_framework.routers import SimpleRouter

from .views import (
    AgregarServicioViewSet,
    AsignarTaxiViewSet,
    AtenderLlamadaViewSet,
    FinalizarAtencionViewSet,
    LlamadaClienteBackViewSet,
    LlamadaClienteViewSet,
    ModificarAtencionViewSet,
    PendienteAtencionViewSet,
    ServiciosDelConductorViewSet,
)

router = SimpleRouter()

app_name = "core_servicio_api"

router.register("llamada-cliente", LlamadaClienteViewSet, basename="llamada_cliente")
router.register(
    "llamada-cliente-back", LlamadaClienteBackViewSet, basename="llamada_cliente_back"
)
router.register("asignar-taxi", AsignarTaxiViewSet, basename="asignar_taxi")
router.register(
    "finalizar-atencion", FinalizarAtencionViewSet, basename="finalizar_atencion"
)
router.register("pen-aten", PendienteAtencionViewSet, basename="pendiente_atencion")
router.register("agregar-servicio", AgregarServicioViewSet, basename="agregar_servicio")
router.register("atender-llamada", AtenderLlamadaViewSet, basename="atiende_llamada")
router.register(
    "modificar-atencion", ModificarAtencionViewSet, basename="modificar_atencion"
)
router.register(
    "conductor-servicios", ServiciosDelConductorViewSet, basename="servicios_conductor"
)

urlpatterns = router.urls
# <slug:uuid_receta>
