from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class ServicioRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class LlamadaRSPagination(DatatablesPageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20
