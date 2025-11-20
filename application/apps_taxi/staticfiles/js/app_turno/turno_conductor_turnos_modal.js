var fnTblEscogerHorarioTurno = null;
var fnTblEscHorarioConductorUncheck = null;
$(document).ready(function () {
  const $tblEscogerHorarioTurno = $("#lista-turno-escoger");
  const $btnBuscarEscogerHorarioTurno = $("#btn-buscar-turnos-escoger");
  const arrayOcultarColumaEscogerHorarioTurnoDatatable = [];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  const btnHtmlBuscar = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  function ocultarColumEscogerHorarioTurnoDatatable() {
    const filas = $("#lista-turno-escoger tbody").find("tr").length;
    if (arrayOcultarColumaEscogerHorarioTurnoDatatable.length === 0) {
      $("#lista-turno-escoger thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turno-escoger tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaEscogerHorarioTurnoDatatable.map((item) =>
        $("#lista-turno-escoger thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaEscogerHorarioTurnoDatatable.map((item) => $("#lista-turno-escoger tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblEscogerHorarioTurno = $tblEscogerHorarioTurno.DataTable({
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
    lengthMenu: [10, 20, 30],
    pagingDelay: 1000,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turnos.listaTurnos,
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
          $btnBuscarEscogerHorarioTurno.html(btnHtmlBuscar).prop("disabled", false);
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
          if (arrayOcultarColumaEscogerHorarioTurnoDatatable.length > 0) {
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
          return `${data.nom_horario} | <span class="text-black-50">${data.cod_horario ?? ""}</span>`;
        },
        width: "100",
        className: "text-left",
        searchable: false,
        orderable: true
      },
      {
        data: function (data) {
          return `[${data.inicio_horario} - ${data.fin_horario}]`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let checkOrNotCheck = TURNO_NO_CHECKET;
          if (typeof $campoBsSelectHorarioCodigo !== "undefined") {
            checkOrNotCheck = (data.cod_horario.toString() === $campoBsSelectHorarioCodigo.val().toString()) ? TURNO_CHECKET : TURNO_NO_CHECKET;
          }
          let cssClasCheck = (checkOrNotCheck === TURNO_CHECKET) ? "btn-success" : "btn-info";
          return `<button type="button" data-codigoconductor="${data.cod_horario}"
                    class="btn btn-sm ${cssClasCheck} seleccionar-conductor">${checkOrNotCheck}</button>`;
        },
        width: "25",
        className: "text-center",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumEscogerHorarioTurnoDatatable();
    }
  });

  tblEscogerHorarioTurno.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblEscogerHorarioTurno.DataTable().page.info();
    tblEscogerHorarioTurno.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turno-escoger tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblEscogerHorarioTurno.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaEscogerHorarioTurnoDatatable.map(
        (item) => `<th>${$("#lista-turno-escoger thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaEscogerHorarioTurnoDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-turno-escoger tbody").on("click", ".seleccionar-conductor", function () {
    const $auxBtnCheck = $(this);
    const estadoIsChecket = ($auxBtnCheck.html() == TURNO_CHECKET);
    $(".seleccionar-conductor").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
    if (!estadoIsChecket) {
      $auxBtnCheck.html(TURNO_CHECKET).removeClass("btn-info").addClass("btn-success");
      if (typeof $campoBsSelectHorarioCodigo !== "undefined") {
        $campoBsSelectHorarioCodigo.val($auxBtnCheck.data("codigoconductor"));
      }
    } else {
      $campoBsSelectHorarioCodigo.val("");
    }
  });

  fnTblEscogerHorarioTurno = function () {
    try {
      tblEscogerHorarioTurno.search("");
      tblEscogerHorarioTurno.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  fnTblEscHorarioConductorUncheck = function () {
    $(".seleccionar-conductor").html(TURNO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
  };

});
