var fnTblDetServConductor = null;
$(document).ready(function () {
  const $tblDetServConductor = $("#lista-detalle-servicios-conductor");
  const arrayOcultarColumaDetServConductorDatatable = [];

  function ocultarColumDatatableDetServConductor() {
    const filas = $("#lista-detalle-servicios-conductor tbody").find("tr").length;
    if (arrayOcultarColumaDetServConductorDatatable.length === 0) {
      $("#lista-detalle-servicios-conductor thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-detalle-servicios-conductor tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaDetServConductorDatatable.map((item) =>
        $("#lista-detalle-servicios-conductor thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaDetServConductorDatatable.map((item) => $("#lista-detalle-servicios-conductor tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblDetServConductor = $tblDetServConductor.DataTable({
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
    lengthMenu: [10, 20],
    pagingDelay: 500,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.servicio.listServiciosConductor,
      method: "get",
      dataType: "json",
      data: function (params) {
        let codigoTurno = $("#id_show_turno_dataid").val();
        params["codigo_turno"] = codigoTurno;
        return params;
      },
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
            location.href = urlAccessList.dashboardPage;
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
        data: function (data) {
          if (arrayOcultarColumaDetServConductorDatatable.length > 0) {
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
          return `${dataCliente.nombre ?? "Anonimo"} <div
                class="label label-table label-info">${dataCliente.servicios_realizados ?? "0"}</div>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let programado = data.hora_programacion ?? "";
          let hora_inicio = data.hora_inicio ?? "";
          let hora_fin = data.hora_fin ?? "*";
          if (hora_inicio) {
            return `<span class="small"><b>&#91;${hora_inicio} - ${hora_fin}&#93;</b></span>`;
          }
          return `<span class="small"><b>Prog.: ${programado}</b></span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `<span class="small">${data.referencia_origen ?? ""}</span> <i
                    class="fa fa-arrow-right text-info"> </i> <span class="small">${data.referencia_destino ?? ""}</span>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let estado = data.estado_atencion ?? "";
          if (estado == "Finalizada") {
            return `<span class="label label-table table-info border border-info text-black-50"
                >${data.estado_atencion ?? ""}</span>`;
          }
          return `<span class="label label-table table-primary border border-primary text-info"
                >${data.estado_atencion ?? ""}</span>`;
        },
        className: "text-center",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableDetServConductor();
    }
  });

  tblDetServConductor.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblDetServConductor.DataTable().page.info();
    tblDetServConductor.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-detalle-servicios-conductor tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblDetServConductor.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaDetServConductorDatatable.map(
        (item) => `<th>${$("#lista-detalle-servicios-conductor thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaDetServConductorDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  fnTblDetServConductor = function () {
    try {
      tblDetServConductor.search("");
      tblDetServConductor.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };

});
