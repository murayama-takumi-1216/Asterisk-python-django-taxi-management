var fnTblEscogerTurno02 = null;
var fnTblEscogerTurno02PageInitial = null;
var fnTblEscogerTurno02SetPageLength = null;
// var fnTblEscTurnoUncheck = null;
$(document).ready(function () {
  const $tblEscogerTurno02 = $("#lista-turnos-escoger-02");
  const arrayOcultarColumaEscogerTurno02Datatable = [0];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  function ocultarColumEscogerTurno02Datatable() {
    const filas = $("#lista-turnos-escoger-02 tbody").find("tr").length;
    if (arrayOcultarColumaEscogerTurno02Datatable.length === 0) {
      $("#lista-turnos-escoger-02 thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turnos-escoger-02 tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaEscogerTurno02Datatable.map((item) =>
        $("#lista-turnos-escoger-02 thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaEscogerTurno02Datatable.map((item) => $("#lista-turnos-escoger-02 tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblEscogerTurno02 = $tblEscogerTurno02.DataTable({
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
        params["length"] = varTblEscogerTurno01_lengthPage;
        if (params.start < varTblEscogerTurno01_lengthPage) {
          params["start"] = varTblEscogerTurno01_lengthPage;
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        return false;
        // swal.fire({
        //   title: "Alerta Turnos por escoger - Carga de datos",
        //   html: `No se llegó conectar con el servidor. <br> ¿Desea volver a cargar la página?`,
        //   type: "warning",
        //   allowOutsideClick: false,
        //   allowEscapeKey: true,
        //   showConfirmButton: true,
        //   showCancelButton: true,
        //   confirmButtonColor: "#3085d6",
        //   cancelButtonColor: "#d33",
        //   confirmButtonText: `<i class="fa fa-check"></i> Permanecer`,
        //   cancelButtonText: `<i class="fa fa-times"></i> Volver a cargar página`
        // }).then(function (isConfirmed) {
        //   if (!isConfirmed.value) {
        //     location.href = urlList.dashboardPage;
        //     return true;
        //   }
        // });
      }
    },
    columns: [
      // {
      //   class: "text-center",
      //   orderable: false,
      //   searchable: false,
      //   data: function (data) {
      //     if (arrayOcultarColumaEscogerTurno02Datatable.length > 0) {
      //       return ``;
      //     }
      //     return "";
      //   },
      //   defaultContent: ""
      // },
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
          return `<button type="button" data-codigoturno="${data.id}"
                data-nombre="${nombreCliente}" data-vehiculo="${vehiculo.nombre}"
                class="btn btn-sm btn-cyan detalle-itinerario-conductor"><i
                class="fa fa-list"></i></button>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
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
          // return `<span class="label label-table label-primary font-bold">${serviciosPendientes}</span>
          //       / <span class="label label-table label-megna font-bold">${data.servicios_atendidos ?? 0}</span>
          //       | <div class="label label-table label-danger">${serviciosCancelado}</div>`;
          return `<span class="label label-table label-megna pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosAtendidos}</span>
                <div class="label label-table label-danger pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosCancelado}</div>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let checkOrNotCheck = TURNO_NO_CHECKET;
          if (typeof $campoAtenderLlamdaServicioTurno !== "undefined") {
            checkOrNotCheck = (data.id.toString() === $campoAtenderLlamdaServicioTurno.val().toString()) ? TURNO_CHECKET : TURNO_NO_CHECKET;
          }
          let cssClasCheck = (checkOrNotCheck === TURNO_CHECKET) ? "btn-success" : "btn-primary";
          return `<button type="button" data-codigoturno="${data.id}"
                    class="btn btn-sm ${cssClasCheck} seleccionar-turno">${checkOrNotCheck}</button>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumEscogerTurno02Datatable();
      $($("#lista-turnos-escoger-02_paginate > ul").children()[1]).hide();
      const pag2 = $($("#lista-turnos-escoger-02_paginate > ul").children()[2]);
      if (!pag2.hasClass("active")) {
        pag2.addClass("active");
      }
    }
  });

  fnTblEscogerTurno02SetPageLength = function (displayLength) {
    var oSettings = tblEscogerTurno02.settings();
    oSettings[0]._iDisplayLength = displayLength;
  }

  $("#lista-turnos-escoger-02 tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblEscogerTurno02.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaEscogerTurno02Datatable.map(
        (item) => `<th>${$("#lista-turnos-escoger-02 thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaEscogerTurno02Datatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-turnos-escoger-02 tbody").on("click", ".seleccionar-turno", function () {
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

  fnTblEscogerTurno02 = function () {
    try {
      tblEscogerTurno02.search("");
      tblEscogerTurno02.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblEscogerTurno02PageInitial = function () {
    tblEscogerTurno02.page(1).draw(false);
  }
  //
  // fnTblEscTurnoUncheck = function () {
  //   $(".seleccionar-turno").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-primary");
  // };

});
