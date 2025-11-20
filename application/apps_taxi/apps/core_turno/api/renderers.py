import logging

from rest_framework_datatables.renderers import (
    DatatablesRenderer as DatatablesRendererBase,
)

logger = logging.getLogger(__name__)


class DatatablesRenderer(DatatablesRendererBase):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view_column = "02"
        row_page = 0
        try:
            view_column = renderer_context.get("request").GET.get("view_column")
            row_page = renderer_context.get("request").GET.get("length", 1)
            row_page = int(row_page)
        except Exception as ex:
            mensaje = "Error verificar view_column en DataTablesRenderes"
            logger.warning(mensaje, exc_info=True, extra={"error_data": str(ex)})

        if view_column and view_column == "01" and row_page > 0:
            records_filtered = data.get("recordsFiltered")
            records_total = data.get("recordsTotal")
            data.update(
                {
                    "recordsFiltered": (
                        records_filtered if records_filtered <= row_page else row_page
                    ),
                    "recordsTotal": (
                        records_total if records_total <= row_page else row_page
                    ),
                    "recordsFilteredReal": records_filtered,
                    "recordsTotalReal": records_total,
                }
            )
        return super().render(data, accepted_media_type, renderer_context)
