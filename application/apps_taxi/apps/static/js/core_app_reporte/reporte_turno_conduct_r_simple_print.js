var fnTblTurnoConductor = null;
$(document).ready(function () {
  const $btnFiltarTurnoConductoresList = $("#btnFiltarTurnoConductoresList");
  const $btnLimpiarFiltroTurnoConductoresList = $("#btnLimpiarFiltroTurnoConductoresList");
  const $tblTurnoConductor = $("#lista-turnos-conductor");
  const arrayOcultarColumaTurnoConductorDatatable = [];

  function ocultarColumDatatableTurnoConductor() {
    const filas = $("#lista-turnos-conductor tbody").find("tr").length;
    if (arrayOcultarColumaTurnoConductorDatatable.length === 0) {
      $("#lista-turnos-conductor thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turnos-conductor tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnoConductorDatatable.map((item) =>
        $("#lista-turnos-conductor thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnoConductorDatatable.map((item) => $("#lista-turnos-conductor tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnoConductor = $tblTurnoConductor.DataTable({
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
    paging: true,
    lengthMenu: [1000, 10000],
    pagingDelay: 1000,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.turnoConductor.listaRSimpleConductores,
      method: "get",
      dataType: "json",
      data: function (params) {
        let codigoVehiculo = $("#id_turncond_nombre_vehiculo").val() ?? 0;
        if (parseInt(codigoVehiculo) > 0) {
          params["filtro_nombre_vehiculo"] = codigoVehiculo;
        }
        let fechaInicio = $("#id_turncond_fecha_inicio").val() ?? "";
        if (fechaInicio.length > 1) {
          params["filtro_fecha_inicio"] = fechaInicio;
        }
        let fechaFin = $("#id_turncond_fecha_fin").val() ?? "";
        if (fechaFin.length > 1) {
          params["filtro_fecha_fin"] = fechaFin;
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
          $btnFiltarTurnoConductoresList.prop("disabled", false);
          $btnLimpiarFiltroTurnoConductoresList.prop("disabled", false);
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
          if (arrayOcultarColumaTurnoConductorDatatable.length > 0) {
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
        width: "25",
        data: function (data) {
          return ``;
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "60",
        data: function (data) {
          let showItem = "0";
          let nombreCliente = `${((data.conductor_data ?? {}).nombre ?? "").toUpperCase()}
           ${((data.conductor_data ?? {}).apellido_paterno ?? "").toUpperCase()}`;
          let vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          return `<button type="button" data-codigoturno="${data.id}"
                data-nombre="${nombreCliente}" data-vehiculo="${vehiculo.nombre}"
                class="btn btn-sm btn-info ver-detalle-servicios-conductor"><i
                class="fa fa-list"></i></button>`;
        }
      },
      {
        data: function (data) {
          let conductor = data.conductor_data ?? {};
          let datosConductor = `${conductor.nombre ?? ""} ${conductor.apellido_paterno ?? ""}`;
          return datosConductor;
        },
        className: "text-left",
        searchable: false,
        orderable: false,
      },
      {
        data: function (data) {
          let vehiculo = data.vehiculo_data ?? {};
          let datosVehiculo = `
            <span class="label label-megna pt-2 pb-2 font-16 font-weight-bold">${vehiculo.nombre}</span>`;
          return datosVehiculo;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "130"
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "70",
        data: function (data) {
          return data.fecha_programacion_view;
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "220",
        data: function (data) {
          let horario = data.horario_data ?? {};
          //return `${horario.nombre ?? ""} <span class="text-black-50">${horario.inicio ?? ""}-${horario.fin ?? ""}</span>`;
          return `${horario.nombre ?? ""}`;
        }
      },
      {
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "110",
        data: function (data) {
          let serviciosAtendidos = parseInt(data.servicios_atendidos ?? "0");
          return serviciosAtendidos;
        }
      },
      {
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "110",
        data: function (data) {
          let serviciosCancelados = parseInt(data.servicios_cancelados ?? "0");
          return serviciosCancelados;
        }
      },
      {
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.monto_generado ?? "*";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.estado_turno_text ?? "*";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.observacion ?? "*";
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableTurnoConductor();
      $btnFiltarTurnoConductoresList.prop("disabled", false);
      $btnLimpiarFiltroTurnoConductoresList.prop("disabled", false);
      $(".filtrar-driver").prop("disabled", false);
    }
  });

  tblTurnoConductor.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblTurnoConductor.DataTable().page.info();
    tblTurnoConductor.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turnos-conductor tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnoConductor.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnoConductorDatatable.map(
        (item) => `<th>${$("#lista-turnos-conductor thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnoConductorDatatable.map((item) => `<td>${datos[item]}</td>`);
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
      fnTblTurnoConductor();
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
  $btnFiltarTurnoConductoresList.click(function () {
    $(this).prop("disabled", true);
    fnTblTurnoConductor();
  });
  $btnLimpiarFiltroTurnoConductoresList.click(function () {
    $(this).prop("disabled", true);
    $("#id_turncond_codigo_conductor").val("");
    $("#id_turncond_nombre_vehiculo").val("");
    $("#id_turncond_estado_turno").val("");
    $("#id_turncond_fecha_inicio").val("");
    $("#id_turncond_fecha_fin").val("");
    $("#id_turncond_codigo_horario").val("");
    fnTblTurnoConductor();
  });

  $("#lista-turnos-conductor tbody").on("click", ".filtrar-driver", function () {
    const $btnFiltrarDriver = $(this);
    $btnLimpiarFiltroTurnoConductoresList.prop("disabled", true);
    $btnFiltarTurnoConductoresList.prop("disabled", true);
    $(".filtrar-driver").prop("disabled", true);
    $("#id_turncond_codigo_conductor").val($btnFiltrarDriver.data("codigoconductor"));
    fnTblTurnoConductor();
  });
  $("#lista-turnos-conductor tbody").on("click", ".ver-detalle-servicios-conductor", function () {
    const $btnShow = $(this);
    fnShowDetailServiciosConductor($btnShow);
  });

  function fnShowDetailServiciosConductor($btnShow = null) {
    const $leyendaForm = $("#detalle-lista-servicios-conductor-leyenda");
    const tituloLeyenda = "DETALLE SERVICIOS DEL CONDUCTOR - TURNO";
    const $campoDato = $("#id_show_turno_dataid");
    if (!($campoDato.val()) || $btnShow.data("codigoturno").toString() !== $campoDato.val()) {
      $("#detalle-lista-servicios-conductor").show();
      $campoDato.val($btnShow.data("codigoturno"));
      $leyendaForm.html(`${tituloLeyenda}: ${$btnShow.data("nombre") ?? ""} / ${$btnShow.data("vehiculo") ?? ""}`);
      fnTblDetServConductor();
    } else {
      $("#detalle-lista-servicios-conductor").hide();
      $campoDato.val("");
      $leyendaForm.html(`${tituloLeyenda}`);
    }
  }

  fnTblTurnoConductor = function () {
    try {
      tblTurnoConductor.search("");
      tblTurnoConductor.ajax.reload(null, true);
      $("#detalle-lista-servicios-conductor").hide();
    } catch (e) {
      console.error(e);
    }
  };
  fnTblTurnoConductor();

});
