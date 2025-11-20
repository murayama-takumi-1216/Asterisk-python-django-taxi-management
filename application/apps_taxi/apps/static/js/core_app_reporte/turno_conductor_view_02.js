var fnTblConductorActivos02 = null;
var fnTblConductorActivos02PageInitial = null;
var fnTblConductorActivos02SetPageLength = null;
$(document).ready(function () {
  const $tblConductorActivos02 = $("#lista-conductores-activos-02");
  const arrayOcultarColumaConductorActivos02Datatable = [0];

  function ocultarColumConductorActivos02Datatable() {
    const filas = $("#lista-conductores-activos-02 tbody").find("tr").length;
    if (arrayOcultarColumaConductorActivos02Datatable.length === 0) {
      $("#lista-conductores-activos-02 thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-conductores-activos-02 tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaConductorActivos02Datatable.map((item) =>
        $("#lista-conductores-activos-02 thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaConductorActivos02Datatable.map((item) => $("#lista-conductores-activos-02 tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblConductorActivos02 = $tblConductorActivos02.DataTable({
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
      url: urlList.turnoConductor.listaConductoresActivos,
      method: "get",
      dataType: "json",
      data: function (params) {
        params["view_column"] = "02";
        params["length"] = varTblConductorActivos01_lengthPage;
        if (params.start < varTblConductorActivos01_lengthPage) {
          params["start"] = varTblConductorActivos01_lengthPage;
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
          return `${nombreCliente}`;
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
      ocultarColumConductorActivos02Datatable();
      $($("#lista-conductores-activos-02_paginate > ul").children()[1]).hide();
      const pag2 = $($("#lista-conductores-activos-02_paginate > ul").children()[2]);
      if (!pag2.hasClass("active")) {
        pag2.addClass("active");
      }
    }
  });

  fnTblConductorActivos02SetPageLength = function (displayLength) {
    var oSettings = tblConductorActivos02.settings();
    oSettings[0]._iDisplayLength = displayLength;
  }

  $("#lista-conductores-activos-02 tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblConductorActivos02.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaConductorActivos02Datatable.map(
        (item) => `<th>${$("#lista-conductores-activos-02 thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaConductorActivos02Datatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  fnTblConductorActivos02PageInitial = function () {
    tblConductorActivos02.page(1).draw(false);
  }
});
