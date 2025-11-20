from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class VehiculoRSPagination(DatatablesPageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 120
