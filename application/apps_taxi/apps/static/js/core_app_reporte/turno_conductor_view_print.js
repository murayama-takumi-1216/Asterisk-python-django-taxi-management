var fnTblConductorActivos01 = null;
$(document).ready(function () {
  const $tblConductorActivos01 = $("#lista-conductores-activos-01");
  const arrayOcultarColumaConductorActivos01Datatable = [];

  function ocultarColumConductorActivos01Datatable() {
    const filas = $("#lista-conductores-activos-01 tbody").find("tr").length;
    if (arrayOcultarColumaConductorActivos01Datatable.length === 0) {
      $("#lista-conductores-activos-01 thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-conductores-activos-01 tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaConductorActivos01Datatable.map((item) =>
        $("#lista-conductores-activos-01 thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaConductorActivos01Datatable.map((item) => $("#lista-conductores-activos-01 tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblConductorActivos01 = $tblConductorActivos01.DataTable({
    language: {url: urlList.dataTablesES},
    layout: {
      topStart: {
        buttons: [
          {
            extend: "excel",
            text: "Guardar excel",
            exportOptions: {
              modifier: {page: "current"}
            }
          },
          {
            extend: "pdf",
            text: "Guardar pdf",
            exportOptions: {
              modifier: {page: "current"}
            }
          },
          {
            extend: "print",
            text: "Imprimir",
            exportOptions: {
              modifier: {page: "current"}
            }
          },
        ]
      }
    },
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: true,
    displayLength: 10000,
    paging: true,
    lengthMenu: [1000, 10000],
    pagingDelay: 300,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turnoConductor.listaConductoresActivos,
      method: "get",
      dataType: "json",
      dataSrc: function (jsonData) {
        let _data = jsonData.data;
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
        class: "text-center",
        orderable: false,
        searchable: false,
        width: "30",
        data: function (data) {
          if (arrayOcultarColumaConductorActivos01Datatable.length > 0) {
            return `<div class="details-control">&nbsp;</div>`;
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
          let dataConductor = data.conductor_data ?? {};
          let nombreConductor = `${(dataConductor.apellido_paterno ?? "").toUpperCase()}
           ${(dataConductor.apellido_materno ?? "").toUpperCase()}, ${(dataConductor.nombre ?? "").toUpperCase()}`;
          return `${nombreConductor}`;
        },
        className: "text-left font-12",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let dataConductor = data.conductor_data ?? {};
          return dataConductor.licencia ?? "";
        },
        className: "text-left font-12",
        searchable: false,
        orderable: false,
        width: "150",
      },
      {
        data: function (data) {
          let data_vehiculo = (data.vehiculo_data ?? {}) ?? {nombre: "-", codigo: "-"};
          return `<button type="button" class="btn btn-sm btn-secondary font-16 font-weight-bold">${data_vehiculo.nombre}</button>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false,
      },
      {
        data: function (data) {
          let data_vehiculo = (data.vehiculo_data ?? {}) ?? {};
          return data_vehiculo.matricula ?? "-";
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let serviciosAtendidos = parseInt(data.servicios_atendidos ?? 0);
          return `<span class="label label-table label-megna pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosAtendidos}</span>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let serviciosCancelado = parseInt(data.servicios_cancelados ?? 0);
          return `<span class="label label-table label-danger pt-2 pb-2 font-16 font-weight-bold text-dark">${serviciosCancelado}</span>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumConductorActivos01Datatable();
    }
  });

  tblConductorActivos01.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblConductorActivos01.DataTable().page.info();
    tblConductorActivos01.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-conductores-activos-01 tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblConductorActivos01.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaConductorActivos01Datatable.map(
        (item) => `<th>${$("#lista-conductores-activos-01 thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaConductorActivos01Datatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  fnTblConductorActivos01 = function () {
    try {
      tblConductorActivos01.search("");
      tblConductorActivos01.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

  setTimeout(function () {
    fnTblConductorActivos01();
  }, 300);

});
