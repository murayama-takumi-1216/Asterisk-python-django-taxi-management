var fnTblEscogerConductor = null;
var fnTblEscConductorUncheck = null;
$(document).ready(function () {
  const $tblEscogerConductor = $("#lista-conductores-escoger");
  const $btnBuscarEscogerConductor = $("#btn-buscar-turnos-escoger");
  const arrayOcultarColumaEscogerConductorDatatable = [];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  const btnHtmlBuscar = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  function ocultarColumEscogerConductorDatatable() {
    const filas = $("#lista-conductores-escoger tbody").find("tr").length;
    if (arrayOcultarColumaEscogerConductorDatatable.length === 0) {
      $("#lista-conductores-escoger thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-conductores-escoger tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaEscogerConductorDatatable.map((item) =>
        $("#lista-conductores-escoger thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaEscogerConductorDatatable.map((item) => $("#lista-conductores-escoger tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblEscogerConductor = $tblEscogerConductor.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: true,
    displayLength: 10,
    paging: true,
    lengthMenu: [10, 20, 30],
    pagingDelay: 1000,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.conductor.listaConductores,
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
            location.href = urlList.dashboardPage;
            return true;
          }
          $btnBuscarEscogerConductor.html(btnHtmlBuscar).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        width: "25",
        data: function (data) {
          if (arrayOcultarColumaEscogerConductorDatatable.length > 0) {
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
        width: "20",
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          return `${data.nombre} ${data.apellido_paterno} | <span class="text-black-50">${data.cod_conductor ?? ""}</span>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.estado_text;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.alquileres_realizados ?? 0} / ${data.alquileres_cancelados ?? 0}`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          if (data.estado !== "04") {
            return `<button type="button" class="btn btn-sm btn-light agregar-alquiler" title="No disponible"
              disabled><i class="fa fa-ban"></i></button>`;
          }
          let checkOrNotCheck = TURNO_NO_CHECKET;
          if (typeof $campoBsSelectConductorCodigo !== "undefined") {
            checkOrNotCheck = (data.cod_conductor.toString() === $campoBsSelectConductorCodigo.val().toString()) ? TURNO_CHECKET : TURNO_NO_CHECKET;
          }
          let cssClasCheck = (checkOrNotCheck === TURNO_CHECKET) ? "btn-success" : "btn-info";
          return `<button type="button" data-codigoconductor="${data.cod_conductor}"
                    class="btn btn-sm ${cssClasCheck} seleccionar-conductor">${checkOrNotCheck}</button>`;
        },
        width: "25",
        className: "text-left",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumEscogerConductorDatatable();
    }
  });

  tblEscogerConductor.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblEscogerConductor.DataTable().page.info();
    tblEscogerConductor.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-conductores-escoger tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblEscogerConductor.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaEscogerConductorDatatable.map(
        (item) => `<th>${$("#lista-conductores-escoger thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaEscogerConductorDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-conductores-escoger tbody").on("click", ".seleccionar-conductor", function () {
    const $auxBtnCheck = $(this);
    const estadoIsChecket = ($auxBtnCheck.html() == TURNO_CHECKET);
    $(".seleccionar-conductor").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
    if (!estadoIsChecket) {
      $auxBtnCheck.html(TURNO_CHECKET).removeClass("btn-info").addClass("btn-success");
      if (typeof $campoBsSelectConductorCodigo !== "undefined") {
        $campoBsSelectConductorCodigo.val($auxBtnCheck.data("codigoconductor"));
      }
    } else {
      $campoBsSelectConductorCodigo.val("");
    }
  });

  fnTblEscogerConductor = function () {
    try {
      tblEscogerConductor.search("");
      tblEscogerConductor.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  fnTblEscConductorUncheck = function () {
    $(".seleccionar-conductor").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
  };

});
