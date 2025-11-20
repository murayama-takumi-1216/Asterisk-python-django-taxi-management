var fnTblPendienteAtencion = null;
$(document).ready(function () {
  const $tblPendAtencion = $("#lista-pendientes-en-atencion");
  const $btnBuscarPendAtencion = $("#btn-buscar-pendientes-en-atencion");
  const arrayOcultarColumaPendAtencionDatatable = [];

  const btnHtmlBuscarPendAtencion = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarPendAtencionLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  const ESTADO_PEN_ATEN_SERVICIO_PENDIENTE = "01";
  const ESTADO_PEN_ATEN_SERVICIO_REALIZADO = "02";
  const ESTADO_PEN_ATEN_SERVICIO_CANCELCLI = "03";
  const ESTADO_PEN_ATEN_SERVICIO_CANCELCOND = "04";
  const ESTADO_PEN_ATEN_SERVICIO_FINALIZADOS = [
    ESTADO_PEN_ATEN_SERVICIO_REALIZADO,
    ESTADO_PEN_ATEN_SERVICIO_CANCELCLI,
    ESTADO_PEN_ATEN_SERVICIO_CANCELCOND,
  ];

  function ocultarColumDatatablePendAtencion() {
    const filas = $("#lista-pendientes-en-atencion tbody").find("tr").length;
    if (arrayOcultarColumaPendAtencionDatatable.length === 0) {
      $("#lista-pendientes-en-atencion thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-pendientes-en-atencion tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaPendAtencionDatatable.map((item) =>
        $("#lista-pendientes-en-atencion thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaPendAtencionDatatable.map((item) => $("#lista-pendientes-en-atencion tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblPendAtencion = $tblPendAtencion.DataTable({
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
      url: urlList.servicio.listPendienteYAtencion,
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
          $btnBuscarPendAtencion.html(btnHtmlBuscarPendAtencion).prop("disabled", false);
          if (!isConfirmed.value) {
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
          if (arrayOcultarColumaPendAtencionDatatable.length > 0) {
            return ``;
          }
          return "";
        },
        defaultContent: ""
      },
      {
        className: "text-center",
        searchable: false,
        width: "20",
        orderable: false,
        data: function (data) {
          return "";
        }
      },
      {
        data: function (data) {
          let dataCliente = data.cliente_data ?? {};
          return dataCliente.telefono ?? "-";
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let dataCliente = data.cliente_data ?? {};
          return `${dataCliente.nombre ?? ""} <div
                >${dataCliente.servicios_realizados ?? "0"}</div>`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `<span>${(data.text_horario ?? "").toString().toUpperCase()}</span> <span
                 title="${data.fecha_programacion}">${data.hora_programacion ?? ""}</span>`;
        },
        className: "text-center font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return `${data.referencia_origen ?? ""} <i class="fa fa-arrow-right text-cyan"> </i> ${data.referencia_destino ?? ""}`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let conductor = ((data.turno_cond_data ?? {}).conductor_data ?? {
            cod_conductor: "-",
            nombre: "-",
            apellido_paterno: "-"
          });
          let vehiculo = ((data.turno_cond_data ?? {}).vehiculo_data ?? {
            cod_vehiculo: "-",
            nom_vehiculo: "-"
          });
          return `<span >${vehiculo.nom_vehiculo}</span>
            ${conductor.nombre} ${conductor.apellido_paterno}`;
        },
        className: "text-left font-weight-bold",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let estado_finalizado = data.estado_finaliza_servicio ?? "";
          if (estado_finalizado == "01") {
            return `<span class="label label-table table-info text-black-50 font-weight-bold"
                >${data.text_estado_finaliza_servicio}</span>`;
          } else if (estado_finalizado == "02") {
            return `<span class="label label-table table-success text-black-50 font-weight-bold"
                >${data.text_estado_finaliza_servicio}</span>`;
          } else {
            return `<span class="label label-table table-primary text-black-50 font-weight-bold"
                >${data.text_estado_finaliza_servicio}</span>`;
          }
        },
        className: "text-center",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          let servicioFinalizado = (ESTADO_PEN_ATEN_SERVICIO_FINALIZADOS.includes(data.estado_finaliza_servicio));
          let codigo_cliente = (data.cliente_data ?? {}).codigo ?? "";
          let nombreVehiculo = ((data.turno_cond_data ?? {}).vehiculo_data ?? {}).nom_vehiculo ?? "";
          let conductorData = (data.turno_cond_data ?? {}).conductor_data ?? {};
          let nombreConductor = `${conductorData.nombre ?? ""} ${conductorData.apellido_paterno ?? ""}`;
          let servicio_id = data.id ?? "";
          let estado_llamada = data.estado_llamada ?? "";
          let btnData = ` data-codigocliente="${codigo_cliente}" data-codigoservicio="${servicio_id}"
              data-nombrevehiculo="${nombreVehiculo}" data-nombreconductor="${nombreConductor}"`;
          let btnVerDetalle = `<button type="button" ${btnData} class="btn btn-sm btn-info detalle-servicio"
              >Detalle</button>`;
          if (servicioFinalizado) {
            return btnVerDetalle;
          }
          let bntAtendido = `<button type="button" ${btnData}
              class="btn btn-sm btn-cyan finalizar-servicio-atendido">Finalizar</button>`;
          let bntCancelaCli = `<button type="button" ${btnData}
              class="btn btn-sm btn-primary finalizar-servicio-cancelcli">Cancelado</button>`;
          let bntModificar = `<button type="button" ${btnData}
              class="btn btn-sm btn-success finalizar-servicio-modificar" title="Modificar">Modificar</button>`;
          return `<div class="btn-group" role="group" aria-label="Opciones">
              ${btnVerDetalle} ${bntModificar}</div>
              <div class="btn-group" role="group" aria-label="Finalizar">${bntAtendido} ${bntCancelaCli}</div>`;
        },
        className: "text-center",
        width: "280",
        searchable: false,
        orderable: false
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatablePendAtencion();
    }
  });

  tblPendAtencion.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblPendAtencion.DataTable().page.info();
    tblPendAtencion.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-pendientes-en-atencion tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblPendAtencion.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaPendAtencionDatatable.map(
        (item) => `<th>${$("#lista-pendientes-en-atencion thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaPendAtencionDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });
  fnTblPendienteAtencion = function () {
    try {
      tblPendAtencion.search("");
      tblPendAtencion.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblPendienteAtencion();

});
