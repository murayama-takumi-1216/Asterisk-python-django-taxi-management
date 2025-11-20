var fnTblTurnosOperador = null;
$(document).ready(function () {
  const $tblTurnosOperador = $("#lista-turnos-operador");
  const arrayOcultarColumaTurnosOperadorDatatable = [];

  const btnHtmlBuscarTurnosOperador = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarTurnosOperadorLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  const ESTADO_TURNO_OPER_PENDIENTE = "01";
  const ESTADO_TURNO_OPER_PROGRAMADO = "02";
  const ESTADO_TURNO_OPER_ACTIVO = "03";
  const ESTADO_TURNO_OPER_CONCLUIDO = "04";
  const ESTADO_TURNO_OPER_CANCELADO = "05";
  const ESTADO_TURNO_OPER_REPROGRAMADO = "06";
  const ESTADO_TURNO_OPER_FINALIZADOS = [
    ESTADO_TURNO_OPER_CONCLUIDO,
    ESTADO_TURNO_OPER_CANCELADO,
    ESTADO_TURNO_OPER_REPROGRAMADO,
  ];

  function ocultarColumDatatableTurnosOperador() {
    const filas = $("#lista-turnos-operador tbody").find("tr").length;
    if (arrayOcultarColumaTurnosOperadorDatatable.length === 0) {
      $("#lista-turnos-operador thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turnos-operador tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnosOperadorDatatable.map((item) =>
        $("#lista-turnos-operador thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnosOperadorDatatable.map((item) => $("#lista-turnos-operador tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnosOperador = $tblTurnosOperador.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: false,
    displayLength: 10,
    paging: true,
    lengthMenu: [10, 20],
    pagingDelay: 500,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.turnoOperador.listTurnos,
      method: "get",
      dataType: "json",
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
            return true;
          }
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumaTurnosOperadorDatatable.length > 0) {
            return ``;
          }
          return "";
        },
        defaultContent: ""
      },
      {
        className: "text-center",
        searchable: false,
        width: "20",
        orderable: false,
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          let dataOperador = data.operador_data ?? {};
          return `${dataOperador.nombre ?? ""} ${dataOperador.apellido_paterno ?? ""}`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let dataCliente = data.cliente_data ?? {};
          return `${data.fecha_programacion ?? ""}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let dataHorario = data.horario_data ?? {};
          return `${dataHorario.nombre ?? ""}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let inicio = data.hora_programacion ?? "";
          if (inicio.length > 0) {
            inicio = inicio.substring(0, 5);
          } else {
            inicio = null;
          }
          let fin = data.hora_fin_programacion ?? "";
          if (fin.length > 0) {
            fin = fin.substring(0, 5);
          } else {
            fin = null;
          }
          return `${inicio ?? "*"} - ${fin ?? "*"}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let inicio = data.hora_inicio ?? "";
          if (inicio.length > 0) {
            inicio = inicio.substring(0, 5);
          } else {
            inicio = null;
          }
          let fin = data.hora_fin ?? "";
          if (fin.length > 0) {
            fin = fin.substring(0, 5);
          } else {
            fin = null;
          }
          return `${inicio ?? "*"} - ${fin ?? "*"}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.llamadas_atendidos ?? "0"}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.servicios_registradas ?? "0"}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.servicios_asignadas ?? "0"}`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          if (ESTADO_TURNO_OPER_FINALIZADOS.includes(data.estado_turno)) {
            return `<span class="label label-table table-info text-black-50">${data.estado_turno_text}</span>`;
          } else if (data.estado_turno == ESTADO_TURNO_OPER_ACTIVO) {
            return `<span class="label label-table table-success text-black-50">${data.estado_turno_text}</span>`;
          } else {
            return `<span class="label label-table table-primary text-black-50">${data.estado_turno_text}</span>`;
          }
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `-`;
        },
        className: "text-center",
        width: "240",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableTurnosOperador();
    }
  });

  tblTurnosOperador.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblTurnosOperador.DataTable().page.info();
    tblTurnosOperador.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turnos-operador tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnosOperador.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnosOperadorDatatable.map(
        (item) => `<th>${$("#lista-turnos-operador thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnosOperadorDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });
  fnTblTurnosOperador = function () {
    try {
      tblTurnosOperador.search("");
      tblTurnosOperador.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblTurnosOperador();

});
