var fnTblResumenServiciosDia = null;
$(document).ready(function () {
  const $btnFiltarResumenServiciosDiaesList = $("#btnFiltarResumenServiciosDiaesList");
  const $btnLimpiarFiltroResumenServiciosDiaList = $("#btnLimpiarFiltroResumenServiciosDiaList");
  const $tblResumenServiciosDia = $("#lista-servicios-resumen");
  const arrayOcultarColumaResumenServiciosDiaDatatable = [0, 1];

  function ocultarColumDatatableResumenServiciosDia() {
    const filas = $("#lista-servicios-resumen tbody").find("tr").length;
    if (arrayOcultarColumaResumenServiciosDiaDatatable.length === 0) {
      $("#lista-servicios-resumen thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-servicios-resumen tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaResumenServiciosDiaDatatable.map((item) =>
        $("#lista-servicios-resumen thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaResumenServiciosDiaDatatable.map((item) => $("#lista-servicios-resumen tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblResumenServiciosDia = $tblResumenServiciosDia.DataTable({
    language: {url: urlList.dataTablesES},
    layout: {
      topStart: {
        buttons: [
          {
            extend: "excel",
            text: "Guardar excel",
            exportOptions: {
              modifier: {page: "all"}  // Export all filtered data
            }
          },
          {
            extend: "pdf",
            text: "Guardar pdf",
            exportOptions: {
              modifier: {page: "all"}  // Export all filtered data
            }
          },
          {
            extend: "print",
            text: "Imprimir",
            exportOptions: {
              modifier: {page: "all"}  // Export all filtered data
            }
          },
        ]
      }
    },
    serverSide: true,
    destroy: true,
    deferRender: false,
    deferLoading: 0,
    searchDelay: 350,
    processing: true,
    searching: false,//false//true:boton
    displayLength: 10000,
    paging: false, //true
    info: false,
    lengthMenu: [1000, 10000],
    pagingDelay: 1000,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.turnoConductor.listaResumenOperador,
      method: "get",
      dataType: "json",
      data: function (params) {
        let fechaActual = $("#id_turncond_fecha_actual").val() ?? "";
        if (fechaActual.length > 1) {
          params["filtro_fecha_actual"] = fechaActual;
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        swal.fire({
          title: "Alerta Turnos por escoger - Carga de datos",
          html: `No se llegó conectar con el servidor. <br> ¿Desea volver a cargar la página?`,
          type: "warning",
          allowOutsideClick: false,
          allowEscapeKey: true,
          showConfirmButton: true,
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: `<i class="fa fa-check"></i> Permanecer`,
          cancelButtonText: `<i class="fa fa-times"></i> Volver a cargar página`
        }).then(function (isConfirmed) {
          if (!isConfirmed.value) {
            location.href = urlAccessList.dashboardPage;
            return true;
          }
          $btnFiltarResumenServiciosDiaesList.prop("disabled", false);
          $btnLimpiarFiltroResumenServiciosDiaList.prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        width: "30",
        data: function (data) {
          if (arrayOcultarColumaResumenServiciosDiaDatatable.length > 0) {
            return `<div class="details-control">&nbsp;</div>`;
          }
          return "";
        },
        defaultContent: ""
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "60",
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          return data.fecha ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false,
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        data: function (data) {
          return `
            <span class="label label-primary pt-2 pb-2 font-16 text-dark font-weight-bold d-inline-block"
             title="Atendidos">${data.llamadas_atendidas ?? "0"}</span>`;
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        data: function (data) {
          return `
            <span class="label label-megna pt-2 pb-2 font-16 text-dark font-weight-bold mr-1 d-inline-block"
             title="Registradas">${data.registrados ?? "0"}</span>`;
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        data: function (data) {
          return `
            <span class="label label-success pt-2 pb-2 text-dark font-16 font-weight-bold mr-1 d-inline-block"
            title="Asignados">${data.asignados ?? "0"}</span>`;
        }
      },
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableResumenServiciosDia();
      $btnFiltarResumenServiciosDiaesList.prop("disabled", false);
      $btnLimpiarFiltroResumenServiciosDiaList.prop("disabled", false);
      $(".filtrar-driver").prop("disabled", false);
      fnTblTurnoOperador();
    }
  });

  tblResumenServiciosDia.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblResumenServiciosDia.DataTable().page.info();
    tblResumenServiciosDia.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-servicios-resumen tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblResumenServiciosDia.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaResumenServiciosDiaDatatable.map(
        (item) => `<th>${$("#lista-servicios-resumen thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaResumenServiciosDiaDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  // Modal
  $("#bs-selec-condcutor-modal-lg").on("show.bs.modal", function () {
    setTimeout(function () {
      // fnTblEscogerConductor();
    }, 300);
  });

  $("#bs-selec-condcutor-modal-lg").on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblResumenServiciosDia();
    }, 300);
  });

  // ----------- rango de fechas  -------------------->
  const fechaDPActual = new Date();
  const fechaDPMinima = new Date();
  fechaDPMinima.setDate(fechaDPMinima.getDate() - 120);
  $("#id_turncond_fecha_inicio").bootstrapMaterialDatePicker({
    format: "YYYY-MM-DD",
    time: false,
    date: true,
    lang: "es-us",
    clearButton: true,
    shortTime: false,
    clearText: "Limpiar",
    cancelText: "Cancelar",
    currentDate: fechaDPActual,
    minDate: fechaDPMinima,
    maxDate: fechaDPActual
  }).change(function () {
    let fechaCampo = moment($("#id_turncond_fecha_inicio").val());
    $("#id_turncond_fecha_fin").bootstrapMaterialDatePicker("setMinDate", fechaCampo.format("YYYY-MM-DD"))
  });

  $("#id_turncond_fecha_fin").bootstrapMaterialDatePicker({
    format: "YYYY-MM-DD",
    time: false,
    date: true,
    lang: "es-us",
    clearButton: true,
    shortTime: false,
    clearText: "Limpiar",
    cancelText: "Cancelar",
    // currentDate: fechaDPActual,
    minDate: fechaDPMinima,
    maxDate: fechaDPActual
  }).change(function () {
    let fechaCampo = moment($("#id_turncond_fecha_fin").val());
    $("#id_turncond_fecha_inicio").bootstrapMaterialDatePicker("setMaxDate", fechaCampo.format("YYYY-MM-DD"))
  });
  // ----------- rango de fechas  <--------------------
  $btnFiltarResumenServiciosDiaesList.click(function () {
    $(this).prop("disabled", true);
    fnTblResumenServiciosDia();
  });
  $btnLimpiarFiltroResumenServiciosDiaList.click(function () {
    $(this).prop("disabled", true);
    $("#id_turncond_fecha_actual").val("");
    fnTblResumenServiciosDia();
  });

  $("#lista-servicios-resumen tbody").on("click", ".filtrar-driver", function () {
    const $btnFiltrarDriver = $(this);
    $btnLimpiarFiltroResumenServiciosDiaList.prop("disabled", true);
    $btnFiltarResumenServiciosDiaesList.prop("disabled", true);
    $(".filtrar-driver").prop("disabled", true);
    $("#id_turncond_codigo_conductor").val($btnFiltrarDriver.data("codigoconductor"));
    fnTblResumenServiciosDia();
  });
  $("#lista-servicios-resumen tbody").on("click", ".ver-detalle-servicios-conductor", function () {
    const $btnShow = $(this);
    fnShowDetailServiciosConductor($btnShow);
  });

  function fnShowDetailServiciosConductor($btnShow = null) {
    const $leyendaForm = $("#detalle-lista-servicios-operador-leyenda");
    const tituloLeyenda = "DETALLE SERVICIOS DEL CONDUCTOR - TURNO";
    const $campoDato = $("#id_show_turno_dataid");
    if (!($campoDato.val()) || $btnShow.data("codigoturno").toString() !== $campoDato.val()) {
      $("#detalle-lista-servicios-operador").show();
      $campoDato.val($btnShow.data("codigoturno"));
      $leyendaForm.html(`${tituloLeyenda}: ${$btnShow.data("nombre") ?? ""} / ${$btnShow.data("vehiculo") ?? ""}`);
      fnTblDetServConductor();
    } else {
      $("#detalle-lista-servicios-operador").hide();
      $campoDato.val("");
      $leyendaForm.html(`${tituloLeyenda}`);
    }
  }

  fnTblResumenServiciosDia = function () {
    try {
      tblResumenServiciosDia.search("");
      tblResumenServiciosDia.ajax.reload(null, true);
      $("#detalle-lista-servicios-operador").hide();
    } catch (e) {
      console.error(e);
    }
  };
  fnTblResumenServiciosDia();

});
