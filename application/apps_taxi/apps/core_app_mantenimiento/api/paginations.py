from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class ConductorRSPagination(DatatablesPageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 60


class VehiculoRSPagination(DatatablesPageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 60


class OperadorRSPagination(DatatablesPageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 60
