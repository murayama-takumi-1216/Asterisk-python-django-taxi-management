from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class TurnoOperadorRSPagination(DatatablesPageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 50
