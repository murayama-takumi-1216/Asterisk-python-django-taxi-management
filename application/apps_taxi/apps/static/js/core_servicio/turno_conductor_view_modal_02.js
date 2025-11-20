var fnTblTurnoConductor02 = null;
var fnTblTurnoConductor02PageInitial = null;
var fnTblTurnoConductor02SetPageLength = null;
// var fnTblEscTurnoUncheck = null;
$(document).ready(function () {
  const $tblTurnoConductor02 = $("#lista-turno-conductor-02");
  const arrayOcultarColumaTurnoConductor02Datatable = [0];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  function ocultarColumTurnoConductor02Datatable() {
    const filas = $("#lista-turno-conductor-02 tbody").find("tr").length;
    if (arrayOcultarColumaTurnoConductor02Datatable.length === 0) {
      $("#lista-turno-conductor-02 thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turno-conductor-02 tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnoConductor02Datatable.map((item) =>
        $("#lista-turno-conductor-02 thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnoConductor02Datatable.map((item) => $("#lista-turno-conductor-02 tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnoConductor02 = $tblTurnoConductor02.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: false,
    displayLength: 30,
    paging: true,
    lengthMenu: [5, 10, 20, 30, 40, 60],
    pagingDelay: 500,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turno.listTurno,
      method: "get",
      dataType: "json",
      data: function (params) {
        params["view_column"] = "02";
        params["length"] = varTblTurnoConductor01_lengthPage;
        if (params.start < varTblTurnoConductor01_lengthPage) {
          params["start"] = varTblTurnoConductor01_lengthPage;
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        return false;
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
      ocultarColumTurnoConductor02Datatable();
      $($("#lista-turno-conductor-02_paginate > ul").children()[1]).hide();
      const pag2 = $($("#lista-turno-conductor-02_paginate > ul").children()[2]);
      if (!pag2.hasClass("active")) {
        pag2.addClass("active");
      }
    }
  });

  fnTblTurnoConductor02SetPageLength = function (displayLength) {
    var oSettings = tblTurnoConductor02.settings();
    oSettings[0]._iDisplayLength = displayLength;
  }

  $("#lista-turno-conductor-02 tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnoConductor02.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnoConductor02Datatable.map(
        (item) => `<th>${$("#lista-turno-conductor-02 thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnoConductor02Datatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-turno-conductor-02 tbody").on("click", ".seleccionar-turno", function () {
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

  fnTblTurnoConductor02 = function () {
    try {
      tblTurnoConductor02.search("");
      tblTurnoConductor02.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblTurnoConductor02PageInitial = function () {
    tblTurnoConductor02.page(1).draw(false);
  }
});
