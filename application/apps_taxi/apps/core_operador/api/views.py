import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer

from apps.common.views import ProtectedAdministradorApiView
from apps.core_operador.models import Operador

from .paginations import OperadorRSPagination
from .serializers import OperadorSerializer

logger = logging.getLogger(__name__)


class OperadorViewSet(ProtectedAdministradorApiView, ModelViewSet):
    serializer_class = OperadorSerializer
    queryset = Operador.objects.all()
    pagination_class = OperadorRSPagination

    filter_backends = [DatatablesFilterBackend]
    renderer_classes = [DatatablesRenderer]

    def filter_queryset(self, queryset):
        queryset = queryset.filter(estado=True).order_by("apellido_paterno")
        return queryset
