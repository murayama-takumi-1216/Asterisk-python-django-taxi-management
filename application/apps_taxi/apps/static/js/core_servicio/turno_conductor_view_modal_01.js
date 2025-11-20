var fnTblTurnoConductor01 = null;
var varTblTurnoConductor01_lengthPage = 0;
var fnTblEscTurnoUncheck = null;
var varTblTurnoConductor01_turnoAutomatico = 0;
$(document).ready(function () {
  const $tblTurnoConductor01 = $("#lista-turno-conductor-01");
  const arrayOcultarColumaTurnoConductor01Datatable = [0];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  function ocultarColumTurnoConductor01Datatable() {
    const filas = $("#lista-turno-conductor-01 tbody").find("tr").length;
    if (arrayOcultarColumaTurnoConductor01Datatable.length === 0) {
      $("#lista-turno-conductor-01 thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turno-conductor-01 tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnoConductor01Datatable.map((item) =>
        $("#lista-turno-conductor-01 thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnoConductor01Datatable.map((item) => $("#lista-turno-conductor-01 tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnoConductor01 = $tblTurnoConductor01.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: true,
    displayLength: 30,
    paging: true,
    lengthMenu: [5, 10, 20, 30, 40, 60],
    pagingDelay: 300,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turno.listTurno,
      method: "get",
      dataType: "json",
      data: function (params) {
        const choicesRowXPag_col02 = "#lista-turno-conductor-02_length select[name=lista-turno-conductor-02_length]";
        params["view_column"] = "01";
        if (varTblTurnoConductor01_lengthPage != parseInt(params.length)) {
          varTblTurnoConductor01_lengthPage = parseInt(params.length);
          $($(choicesRowXPag_col02)[0]).val(varTblTurnoConductor01_lengthPage);
          $($(choicesRowXPag_col02)[0]).prop("disabled", true);
          fnTblTurnoConductor02SetPageLength(varTblTurnoConductor01_lengthPage);
        }
        if (varTblTurnoConductor01_turnoAutomatico === 1) {
          params["turno_automatico"] = varTblTurnoConductor01_turnoAutomatico;
          varTblTurnoConductor01_turnoAutomatico = 0;
        }
        return params;
      },
      dataSrc: function (jsonData) {
        let _data = jsonData.data;
        let recordReal = jsonData.recordsTotalReal ?? 0;
        if (recordReal > 0 && recordReal > varTblTurnoConductor01_lengthPage)
          setTimeout(function () {
            fnTblTurnoConductor02PageInitial();
          }, 300);
        return _data;
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
            location.href = urlList.dashboardPage;
            return true;
          }
        });
      }
    },
    columns: [
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
          let nombreCliente = `${((data.conductor_data ?? {}).nombre ?? "").toUpperCase()}
           ${((data.conductor_data ?? {}).apellido_paterno ?? "").toUpperCase()}`;
          let vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          return `<span class="font-bold">${nombreCliente}</span>`;
        },
        className: "text-left font-12",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let data_vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          return `<button type="button" class="btn btn-sm btn-secondary font-16 font-weight-bold">${data_vehiculo.nombre}</button>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let telefono = (data.conductor_data ?? {}).telefono ?? "-";
          let direccion = (data.conductor_data ?? {}).direccion ?? "-";
          return `<span class="label label-table label-default font-14 text-dark" title="direccion: ${direccion}">${telefono}</span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let serviciosPendientes = parseInt(data.servicios_asignados ?? 0);
          let serviciosCancelado = parseInt(data.servicios_cancelados ?? 0);
          let serviciosAtendidos = parseInt(data.servicios_atendidos ?? 0);
          return `<span class="label label-table label-megna pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosAtendidos}</span>
                <div class="label label-table label-danger pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosCancelado}</div>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumTurnoConductor01Datatable();
    }
  });

  $("#lista-turno-conductor-01 tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnoConductor01.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnoConductor01Datatable.map(
        (item) => `<th>${$("#lista-turno-conductor-01 thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnoConductor01Datatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-turno-conductor-01 tbody").on("click", ".seleccionar-turno", function () {
    const $auxBtnCheck = $(this);
    const estadoIsChecket = ($auxBtnCheck.html() == TURNO_CHECKET);
    $(".seleccionar-turno").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-primary");
    if (!estadoIsChecket) {
      $auxBtnCheck.html(TURNO_CHECKET).removeClass("btn-primary").addClass("btn-success");
      if (typeof $campoAtenderLlamdaServicioTurno !== "undefined") {
        $campoAtenderLlamdaServicioTurno.val($auxBtnCheck.data("codigoturno"));
      }
    } else {
      $campoAtenderLlamdaServicioTurno.val("");
    }
  });

  fnTblTurnoConductor01 = function () {
    try {
      tblTurnoConductor01.search("");
      tblTurnoConductor01.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  fnTblEscTurnoUncheck = function () {
    $(".seleccionar-turno").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-primary");
  };

});
