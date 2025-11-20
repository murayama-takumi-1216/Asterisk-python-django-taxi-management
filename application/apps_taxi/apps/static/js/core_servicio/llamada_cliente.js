var fnTblLlamadaCliente = null;
var fnRefreshLlamadasCliente = null;
$(document).ready(function () {
  const $tblLlamadaCliente = $("#lista-llamada-cliente");
  const $btnBuscarLlamadaCliente = $("#btn-buscar-llamada-cliente");
  const arrayOcultarColumaLlamadaClienteDatatable = [];

  const ESTADO_LLAMADA_ENTRANTE = "01"
  const ESTADO_LLAMADA_LLAMANDO = "02"
  const ESTADO_LLAMADA_PERDIDA = "03"
  const ESTADO_LLAMADA_CONTESTADA = "04"
  const ESTADO_LLAMADA_ATENDIDO = "05"

  const btnHtmlBuscarLlamadaCliente = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLlamadaClienteLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  var amiMarcatiempoActual = null;
  var refreshAutomaticoLlamadasClienteActivo = false;

  function ocultarColumDatatableLlamadaCliente() {
    const filas = $("#lista-llamada-cliente tbody").find("tr").length;
    if (arrayOcultarColumaLlamadaClienteDatatable.length === 0) {
      $("#lista-llamada-cliente thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-llamada-cliente tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaLlamadaClienteDatatable.map((item) =>
        $("#lista-llamada-cliente thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaLlamadaClienteDatatable.map((item) => $("#lista-llamada-cliente tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblLlamadaCliente = $tblLlamadaCliente.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: false,
    deferLoading: 0,
    searchDelay: 350,
    processing: true,
    searching: false,
    displayLength: 5,
    paging: true,
    lengthMenu: [5, 10, 20],
    pagingDelay: 350,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.llamada.listLlamadaCliente,
      method: "get",
      dataType: "json",
      data: function (params) {
        refreshAutomaticoLlamadasClienteActivo = false;
        return params;
      },
      dataSrc: function (jsonData) {
        refreshAutomaticoLlamadasClienteActivo = true;
        let dataSrc = jsonData.data;
        let dataIni = dataSrc[0] ?? {};
        let marcaTimeAmi = parseInt(dataIni.marca_tiempo_ami ?? 0);
        if (!amiMarcatiempoActual) {
          amiMarcatiempoActual = marcaTimeAmi;
        } else if (marcaTimeAmi > amiMarcatiempoActual) {
          amiMarcatiempoActual = marcaTimeAmi;
        }
        return dataSrc;
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
          $btnBuscarLlamadaCliente.html(btnHtmlBuscarLlamadaCliente).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumaLlamadaClienteDatatable.length > 0) {
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
        width: "20",
        data: function (data) {
          return ``;
        }
      },
      {
        data: function (datos) {
          let servicios = (datos.cliente_data ?? {}).servicios_realizados ?? 0;
          let nombre = (datos.cliente_data ?? {}).nombre ?? null;
          let telefono = datos.numero ?? "Anónimo";
          let fecha = ((datos.fecha_llamada ?? "").substring(2, 10)).replaceAll("-", "/");
          let hora = (datos.hora_llamada ?? "").substring(0, 8);
          // return `${nombre ?? telefono} <div class="label label-table label-primary">${servicios}</div>
          //       | <span class="text-black-50">${fecha} ${hora}</span>`;
          return `${nombre ?? telefono} <div class="label label-table label-primary">${servicios}</div>
                <span class="text-black-50" title="${datos.fecha_llamada ?? ""}">${hora}</span>`;
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        data: function (data) {
          let rutaA = data.nombre ?? null;
          let rutaB = data.nombre ?? null;
          if (rutaA && rutaB) {
            return `${rutaA} <div class="label label-table label-primary">&nbsp;</div> ${rutaA}`;
          } else {
            return `Cliente nuevo`;
          }
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "120",
        data: function (data) {
          let codigo_cliente = (data.cliente_data ?? {}).codigo ?? "";
          let numero_id = data.id ?? "";
          let estado_llamada = data.estado_llamada ?? "";
          let marcaTimeAmi = parseInt(data.marca_tiempo_ami ?? 0);
          if (amiMarcatiempoActual > 1200) {
            if (1200 <= (amiMarcatiempoActual - marcaTimeAmi)) {
              return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-danger llamadas-llamar"><i class="fa fa-phone"></i> llamar</button>`
            }
          }
          if (estado_llamada === ESTADO_LLAMADA_ENTRANTE) {
            if (120 <= (amiMarcatiempoActual - marcaTimeAmi)) {
              return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-danger llamadas-llamar"><i class="fa fa-phone"></i> llamar</button>`
            }
            return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-primary llamadas-contestar"><i class="fa fa-phone"></i> Contestar</button>`;
          } else if (estado_llamada === ESTADO_LLAMADA_LLAMANDO) {
            // return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
            //         class="btn btn-sm btn-warning llamadas-cancelar"><i class="fa fa-phone"></i> Llamando</button>`;
            return `<button type="button" disabled="disabled" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-warning llamadas-cancelar"><i class="fa fa-phone"></i> Llamando</button>`;
          } else if (estado_llamada === ESTADO_LLAMADA_PERDIDA) {
            return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-danger llamadas-llamar"><i class="fa fa-phone"></i> llamar</button>`;
          } else if ([ESTADO_LLAMADA_CONTESTADA, ESTADO_LLAMADA_ATENDIDO].includes(estado_llamada)) {
            return `<button type="button" data-codigocliente="${codigo_cliente}" data-numero_id="${numero_id}"
                    class="btn btn-sm btn-secondary llamadas-contestar"><i class="fa fa-edit"></i> Modificar</button>`;
          } else {
            return "-";
          }
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableLlamadaCliente();
    }
  });

  tblLlamadaCliente.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblLlamadaCliente.DataTable().page.info();
    tblLlamadaCliente.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-llamada-cliente tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblLlamadaCliente.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaLlamadaClienteDatatable.map(
        (item) => `<th>${$("#lista-llamada-cliente thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaLlamadaClienteDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  fnTblLlamadaCliente = function () {
    try {
      tblLlamadaCliente.search("");
      tblLlamadaCliente.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblLlamadaCliente();

  // set timeOut ------------>
  var setIntervalRefreshLlamadasCliente = null;
  fnRefreshLlamadasCliente = function (opcionActivar = "SI") {
    if (opcionActivar == "SI") {
      setIntervalRefreshLlamadasCliente = setInterval(function () {
        if (refreshAutomaticoLlamadasClienteActivo) {
          fnTblLlamadaCliente();
        }
      }, (REFRESH_LLAMADAS_OPERADOR * 1000));
    } else {
      clearInterval(setIntervalRefreshLlamadasCliente);
    }
  }
  fnRefreshLlamadasCliente("SI");

  // set timeOut <------------

  function fnActualizarLlamadaBack() {
    let _url = urlList.llamada.listLlamadaClientBack;
    $.ajax({
      url: _url,
      type: "GET",
      dataType: "json",
      beforeSend: function () {
        $("#bntRefreshBackLlamadas").prop("disabled", true);
      },
      success: function (resp) {
        $("#bntRefreshBackLlamadas").prop("disabled", false);
        let respChannelsComplete = ((resp.data ?? {}).CoreShowChannelsComplete ?? [])[0] ?? {ListItems: 0};
        if (respChannelsComplete.ListItems > 0) {
          fnTblLlamadaCliente();
        }
      },
      error: function (request, status, data) {
        $("#bntRefreshBackLlamadas").prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al contestar la llamada";
        }
      }
    });
  }

  $("#bntRefreshBackLlamadas").click(function () {
    $("#bntRefreshBackLlamadas").prop("disabled", true);
    fnTblLlamadaCliente();
    setTimeout(function () {
      $("#bntRefreshBackLlamadas").prop("disabled", false);
    }, 500)
  });

});
