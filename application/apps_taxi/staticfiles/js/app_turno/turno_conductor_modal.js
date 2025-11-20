var fnTblEscogerTurno = null;
var fnTblEscTurnoUncheck = null;
$(document).ready(function () {
  const $tblEscogerTurno = $("#lista-turnos-escoger");
  const $btnBuscarEscogerTurno = $("#btn-buscar-turnos-escoger");
  const arrayOcultarColumaEscogerTurnoDatatable = [];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  const btnHtmlBuscar = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  function ocultarColumEscogerTurnoDatatable() {
    const filas = $("#lista-turnos-escoger tbody").find("tr").length;
    if (arrayOcultarColumaEscogerTurnoDatatable.length === 0) {
      $("#lista-turnos-escoger thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turnos-escoger tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaEscogerTurnoDatatable.map((item) =>
        $("#lista-turnos-escoger thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaEscogerTurnoDatatable.map((item) => $("#lista-turnos-escoger tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblEscogerTurno = $tblEscogerTurno.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: false,
    displayLength: 2,
    paging: true,
    lengthMenu: [2, 10, 20],
    pagingDelay: 500,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turno.listTurno,
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
          if (!isConfirmed) {
            location.href = urlList.dashboardPage;
            return true;
          }
          $btnBuscarEscogerTurno.html(btnHtmlBuscar).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumaEscogerTurnoDatatable.length > 0) {
            return ``;
          }
          return "";
        },
        defaultContent: ""
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          let showItem = "0";
          let nombreCliente = `${((data.conductor_data ?? {}).nombre ?? "").toUpperCase()}
           ${((data.conductor_data ?? {}).apellido_paterno ?? "").toUpperCase()}`;
          let vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          let serviciosRealizados = (data.servicios_asignados ?? 0) + (data.servicios_atendidos ?? 0);
          return `<button type="button" data-codigoturno="${data.id}"
                data-nombre="${nombreCliente}" data-vehiculo="${vehiculo.nombre}"
                class="btn btn-sm btn-cyan detalle-itinerario-conductor"><i
                class="fa fa-list"></i></button> ${nombreCliente}
                <div class="label label-table label-megna">${serviciosRealizados}</div>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let data_vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          return `<span class="font-weight-bold">${data_vehiculo.nombre}</span> | <span
                    class="small">${data_vehiculo.codigo}</span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.servicios_asignados ?? 0} / ${data.servicios_atendidos ?? 0}`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let checkOrNotCheck = TURNO_NO_CHECKET;
          if (typeof $campoAtenderLlamdaServicioTurno !== "undefined") {
            checkOrNotCheck = (data.id.toString() === $campoAtenderLlamdaServicioTurno.val().toString()) ? TURNO_CHECKET : TURNO_NO_CHECKET;
          }
          let cssClasCheck = (checkOrNotCheck === TURNO_CHECKET) ? "btn-success" : "btn-info";
          return `<button type="button" data-codigoturno="${data.id}"
                    class="btn btn-sm ${cssClasCheck} seleccionar-turno">${checkOrNotCheck}</button>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumEscogerTurnoDatatable();
    }
  });

  tblEscogerTurno.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblEscogerTurno.DataTable().page.info();
    tblEscogerTurno.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turnos-escoger tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblEscogerTurno.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaEscogerTurnoDatatable.map(
        (item) => `<th>${$("#lista-turnos-escoger thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaEscogerTurnoDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-turnos-escoger tbody").on("click", ".seleccionar-turno", function () {
    const $auxBtnCheck = $(this);
    const estadoIsChecket = ($auxBtnCheck.html() == TURNO_CHECKET);
    $(".seleccionar-turno").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
    if (!estadoIsChecket) {
      $auxBtnCheck.html(TURNO_CHECKET).removeClass("btn-info").addClass("btn-success");
      if (typeof $campoAtenderLlamdaServicioTurno !== "undefined") {
        $campoAtenderLlamdaServicioTurno.val($auxBtnCheck.data("codigoturno"));
      }
    } else {
      $campoAtenderLlamdaServicioTurno.val("");
    }
  });

  fnTblEscogerTurno = function () {
    try {
      tblEscogerTurno.search("");
      tblEscogerTurno.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  fnTblEscTurnoUncheck = function () {
    $(".seleccionar-turno").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
  };

});
