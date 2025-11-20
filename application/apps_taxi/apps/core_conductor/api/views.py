import logging

from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.views import ProtectedAdministradorApiView
from apps.core_conductor.constants import CONDUCTOR_ESTADO_DISPONIBLE
from apps.core_conductor.models import Conductor

from .paginations import ConductorRSPagination
from .serializers import ConductorSerializer

logger = logging.getLogger(__name__)


class ListaConductorParaAlquilerViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = ConductorSerializer
    queryset = Conductor.objects.all()
    pagination_class = ConductorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        search_term = self.request.query_params.get("search[value]", None)
        queryset = queryset.filter(estado=CONDUCTOR_ESTADO_DISPONIBLE)
        # estado__in=[CONDUCTOR_ESTADO_DISPONIBLE, CONDUCTOR_ESTADO_OCUPADO]
        if search_term:
            queryset = queryset.filter(
                Q(cod_conductor__istartswith=search_term)
                | Q(nombre__istartswith=search_term)
                | Q(apellido_paterno__istartswith=search_term)
                | Q(apellido_materno__istartswith=search_term)
                | Q(licencia__istartswith=search_term)
            )
        return queryset.order_by("nombre", "apellido_paterno")
