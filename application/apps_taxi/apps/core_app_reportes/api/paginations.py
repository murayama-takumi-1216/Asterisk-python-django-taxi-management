from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class TurnoConductorRSPagination(DatatablesPageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 500


class TurnoOperadorRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 60


class ServiciosDiaRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 60


class ServicioRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 40


class TurnoConductorViewRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class DriverVigentesRSPagination(DatatablesPageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 500
