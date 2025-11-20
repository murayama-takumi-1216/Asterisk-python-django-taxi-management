var fnTblAsignarTaxi = null;
$(document).ready(function () {
  const $tblAsignarTaxi = $("#lista-asignar-taxi");
  const $btnBuscarAsignarTaxi = $("#btn-buscar-pendientes-en-atencion");
  const arrayOcultarColumaAsignarTaxiDatatable = [];

  const btnHtmlBuscarAsignarTaxi = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarAsignarTaxiLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  function ocultarColumDatatableAsignarTaxi() {
    const filas = $("#lista-asignar-taxi tbody").find("tr").length;
    if (arrayOcultarColumaAsignarTaxiDatatable.length === 0) {
      $("#lista-asignar-taxi thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-asignar-taxi tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaAsignarTaxiDatatable.map((item) =>
        $("#lista-asignar-taxi thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaAsignarTaxiDatatable.map((item) => $("#lista-asignar-taxi tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblAsignarTaxi = $tblAsignarTaxi.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: false,
    displayLength: 5,
    paging: true,
    lengthMenu: [5, 10, 20],
    pagingDelay: 500,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.servicio.listAsignarTaxi,
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
          $btnBuscarAsignarTaxi.html(btnHtmlBuscarAsignarTaxi).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumaAsignarTaxiDatatable.length > 0) {
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
          let dataCliente = data.cliente_data ?? {};
          // return `${dataCliente.nombre ?? "Anonimo"} <div
          //       class="label label-table label-success">${dataCliente.servicios_realizados ?? "0"}</div>`;
          return `${dataCliente.nombre ?? "Anonimo"}`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          // return `<span class="small">${data.fecha_programacion ?? ""}</span> <span
          //       class="small">${data.hora_programacion ?? ""}</span>`;
          return `<span>${data.hora_programacion ?? ""}</span>`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `<span>${data.referencia_origen ?? ""}</span> <i> </i> <span>${data.referencia_destino ?? ""}</span>`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let codigo_cliente = (data.cliente_data ?? {}).codigo ?? "";
          let servicio_id = data.id ?? "";
          let estado_llamada = data.estado_llamada ?? "";
          return `<button type="button" data-codigocliente="${codigo_cliente}" data-codigoservicio="${servicio_id}"
                    class="btn btn-sm btn-success asignar-taxi"><i class="fa fa-edit"></i> Modificar</button>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableAsignarTaxi();
    }
  });

  tblAsignarTaxi.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblAsignarTaxi.DataTable().page.info();
    tblAsignarTaxi.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-asignar-taxi tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblAsignarTaxi.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaAsignarTaxiDatatable.map(
        (item) => `<th>${$("#lista-asignar-taxi thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaAsignarTaxiDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  fnTblAsignarTaxi = function () {
    try {
      tblAsignarTaxi.search("");
      tblAsignarTaxi.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblAsignarTaxi();


});
