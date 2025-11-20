var fnTblEscogerTurnoOpe = null;
var fnTblEscTurnoOpeUncheck = null;
$(document).ready(function () {
  const $tblEscogerTurnoOpe = $("#lista-operadores-escoger");
  const $btnBuscarEscogerTurnoOpe = $("#btn-buscar-turnos-escoger");
  const arrayOcultarColumEscogerTurnoOpeDatatable = [];

  const SELEC_OPERARIO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const SELEC_OPERARIO_CHECKET = `<i class="fa fa-check"></i>`;

  const btnHtmlBuscar = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  function ocultarColumEscogerTurnoOpeDatatable() {
    const filas = $("#lista-operadores-escoger tbody").find("tr").length;
    if (arrayOcultarColumEscogerTurnoOpeDatatable.length === 0) {
      $("#lista-operadores-escoger thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-operadores-escoger tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumEscogerTurnoOpeDatatable.map((item) =>
        $("#lista-operadores-escoger thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumEscogerTurnoOpeDatatable.map((item) => $("#lista-operadores-escoger tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblEscogerTurnoOpe = $tblEscogerTurnoOpe.DataTable({
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
    lengthMenu: [10, 15, 20],
    pagingDelay: 500,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.operador.listOperadores,
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
          $btnBuscarEscogerTurnoOpe.html(btnHtmlBuscar).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumEscogerTurnoOpeDatatable.length > 0) {
            return ``;
          }
          return "";
        },
        defaultContent: ""
      },
      {
        className: "text-center",
        width: "20",
        searchable: false,
        orderable: false,
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          let nombreCliente = `<span>${(data.nombre ?? "").toUpperCase()}
           ${(data.apellido_paterno ?? "").toUpperCase()}</span>`;
          return nombreCliente;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `<span class="text-black-50">${data.alias ?? "-"}</span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `<span class="text-black-50">${data.user ?? "-"}</span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let checkOrNotCheck = SELEC_OPERARIO_NO_CHECKET;
          if (typeof $campoBsSeleccionarOperador !== "undefined") {
            checkOrNotCheck = (data.codigo.toString() === $campoBsSeleccionarOperador.val().toString()) ? SELEC_OPERARIO_CHECKET : SELEC_OPERARIO_NO_CHECKET;
          }
          let cssClasCheck = (checkOrNotCheck === SELEC_OPERARIO_CHECKET) ? "btn-success" : "btn-info";
          return `<button type="button" data-codigooperario="${data.codigo}"
                    class="btn btn-sm ${cssClasCheck} seleccionar-turno">${checkOrNotCheck}</button>`;
        },
        width: "60",
        className: "text-center",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumEscogerTurnoOpeDatatable();
    }
  });

  tblEscogerTurnoOpe.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblEscogerTurnoOpe.DataTable().page.info();
    tblEscogerTurnoOpe.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-operadores-escoger tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblEscogerTurnoOpe.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumEscogerTurnoOpeDatatable.map(
        (item) => `<th>${$("#lista-operadores-escoger thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumEscogerTurnoOpeDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-operadores-escoger tbody").on("click", ".seleccionar-turno", function () {
    const $auxBtnCheck = $(this);
    const estadoIsChecket = ($auxBtnCheck.html() == SELEC_OPERARIO_CHECKET);
    $(".seleccionar-turno").html(SELEC_OPERARIO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
    if (!estadoIsChecket) {
      $auxBtnCheck.html(SELEC_OPERARIO_CHECKET).removeClass("btn-info").addClass("btn-success");
      if (typeof $campoBsSeleccionarOperador !== "undefined") {
        $campoBsSeleccionarOperador.val($auxBtnCheck.data("codigooperario"));
      }
    } else {
      $campoBsSeleccionarOperador.val("");
    }
  });

  fnTblEscogerTurnoOpe = function () {
    try {
      tblEscogerTurnoOpe.search("");
      tblEscogerTurnoOpe.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  fnTblEscTurnoOpeUncheck = function () {
    $(".seleccionar-turno").html(SELEC_OPERARIO_NO_CHECKET).removeClass("btn-success").addClass("btn-info");
  };

});
