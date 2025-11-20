var fnTblTurnoOperador = null;
$(document).ready(function () {
  const $btnFiltarTurnoOperadoresList = $("#btnFiltarTurnoOperadoresList");
  const $btnLimpiarFiltroTurnoOperadorList = $("#btnLimpiarFiltroTurnoOperadorList");
  const $tblTurnoOperador = $("#lista-turnos-operador");
  const arrayOcultarColumaTurnoOperadorDatatable = [0, 1];

  function ocultarColumDatatableTurnoOperador() {
    const filas = $("#lista-turnos-operador tbody").find("tr").length;
    if (arrayOcultarColumaTurnoOperadorDatatable.length === 0) {
      $("#lista-turnos-operador thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turnos-operador tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnoOperadorDatatable.map((item) =>
        $("#lista-turnos-operador thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnoOperadorDatatable.map((item) => $("#lista-turnos-operador tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnoOperador = $tblTurnoOperador.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: false,
    deferLoading: 0,
    searchDelay: 350,
    processing: true,
    searching: false,//false//true:boton
    displayLength: 30,
    paging: true,
    lengthMenu: [10, 20, 30, 40, 60],
    pagingDelay: 1000,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.turnoConductor.listaRSimpleOperador,
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
          $btnFiltarTurnoOperadoresList.prop("disabled", false);
          $btnLimpiarFiltroTurnoOperadorList.prop("disabled", false);
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
          if (arrayOcultarColumaTurnoOperadorDatatable.length > 0) {
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
          let operador = data.operador_data ?? {};
          let datosOperador = `${operador.nombre ?? ""} ${operador.apellido_paterno ?? ""}`;
          return datosOperador;
        },
        className: "text-left",
        searchable: false,
        orderable: false,
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
          return `${horario.nombre ?? ""}`;
        }
      },
      {
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "210",
        data: function (data) {
          let serviciosAtendidos = parseInt(data.llamadas_atendidos ?? "0");
          let serviciosRegistrados = parseInt(data.servicios_registradas ?? "0");
          let serviciosAsignadas = parseInt(data.servicios_asignadas ?? "0");
          let htmlAtendidos = `
            <span class="label label-primary pt-2 pb-2 font-16 text-dark font-weight-bold d-inline-block"
             title="Atendidos">${serviciosAtendidos}</span>`;
          let htmlRegistradas = `
            <span class="label label-megna pt-2 pb-2 font-16 text-dark font-weight-bold mr-1 d-inline-block"
             title="Registradas">${serviciosRegistrados}</span>`;
          let htmlAsignadas = `
            <span class="label label-success pt-2 pb-2 font-16 text-dark font-weight-bold mr-1 d-inline-block"
            title="Asignados">${serviciosAsignadas}</span>`;
          let htmlServicios = `${htmlAtendidos} ${htmlRegistradas} ${htmlAsignadas}`;
          return htmlServicios;
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
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableTurnoOperador();
      $btnFiltarTurnoOperadoresList.prop("disabled", false);
      $btnLimpiarFiltroTurnoOperadorList.prop("disabled", false);
      $(".filtrar-driver").prop("disabled", false);
    }
  });

  tblTurnoOperador.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblTurnoOperador.DataTable().page.info();
    tblTurnoOperador.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turnos-operador tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnoOperador.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnoOperadorDatatable.map(
        (item) => `<th>${$("#lista-turnos-operador thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnoOperadorDatatable.map((item) => `<td>${datos[item]}</td>`);
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
      fnTblTurnoOperador();
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
  $btnFiltarTurnoOperadoresList.click(function () {
    $(this).prop("disabled", true);
    fnTblTurnoOperador();
  });
  $btnLimpiarFiltroTurnoOperadorList.click(function () {
    $(this).prop("disabled", true);
    $("#id_turncond_fecha_actual").val("");
    fnTblTurnoOperador();
  });

  $("#lista-turnos-operador tbody").on("click", ".filtrar-driver", function () {
    const $btnFiltrarDriver = $(this);
    $btnLimpiarFiltroTurnoOperadorList.prop("disabled", true);
    $btnFiltarTurnoOperadoresList.prop("disabled", true);
    $(".filtrar-driver").prop("disabled", true);
    $("#id_turncond_codigo_conductor").val($btnFiltrarDriver.data("codigoconductor"));
    fnTblTurnoOperador();
  });
  $("#lista-turnos-operador tbody").on("click", ".ver-detalle-servicios-conductor", function () {
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

  fnTblTurnoOperador = function () {
    try {
      tblTurnoOperador.search("");
      tblTurnoOperador.ajax.reload(null, true);
      $("#detalle-lista-servicios-operador").hide();
    } catch (e) {
      console.error(e);
    }
  };
  // fnTblTurnoOperador();

});
