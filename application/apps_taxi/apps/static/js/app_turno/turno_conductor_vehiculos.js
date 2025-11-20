var fnTblTurnoVehiculo = null;
const $campoBsSelectHorarioCodigo = $("#id_bs_select_horario_codigo");

$(document).ready(function () {
  const $campoBsSelectTurnoCodigo = $("#id_bs_select_turno_codigo");
  const $campoBsSelectVehiculoCodigo = $("#id_bs_select_vehiculo_codigo");
  const $campoBsSelectConductorCodigo = $("#id_bs_select_conductor_codigo");

  const $idTurnoCheckOpcFinalizar = $("#idTurnoCheckOpcFinalizar");
  const $idTurnoCampoFinalizar = $("#id_turno_finalizar");
  const $btnTurnoConductorFinalizar = $("#btnTurnoConductorFinalizar");

  const $btnFrmTurnoConductorGuardar = $("#btnFrmTurnoConductorGuardar");
  const $btnFrmTurnoConductorCancelar = $("#btnFrmTurnoConductorCancelar");

  const $tblTurnoVehiculo = $("#lista-turno-vehiculo");
  const arrayOcultarColumaTurnoVehiculoDatatable = [];

  function ocultarColumDatatableTurnoVehiculo() {
    const filas = $("#lista-turno-vehiculo tbody").find("tr").length;
    if (arrayOcultarColumaTurnoVehiculoDatatable.length === 0) {
      $("#lista-turno-vehiculo thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-turno-vehiculo tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaTurnoVehiculoDatatable.map((item) =>
        $("#lista-turno-vehiculo thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaTurnoVehiculoDatatable.map((item) => $("#lista-turno-vehiculo tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblTurnoVehiculo = $tblTurnoVehiculo.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: false,
    deferLoading: 0,
    searchDelay: 350,
    processing: true,
    searching: true,//false//true:boton
    displayLength: 10,
    paging: true,
    lengthMenu: [10, 20, 30, 60, 120],
    pagingDelay: 1000,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.vehiculo.listaVehiculo,
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
          if (arrayOcultarColumaTurnoVehiculoDatatable.length > 0) {
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
        width: "25",
        data: function (data) {
          return ``;
        }
      },
      {
        data: function (data) {
          return `<span class="label label-megna font-bold">${data.nom_vehiculo}</span> | <span class="text-black-50">${data.cod_vehiculo}</span>`
        },
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "120"
      },
      {
        className: "text-left border-left border-right",
        searchable: false,
        orderable: false,
        width: "380",
        data: function (data) {
          let contarTurnos = Object.keys(data.turno_data ?? {}).length;
          let alquileres = data.alquiler_data ?? {};
          let conductor = {};
          let alquiler = {};
          let nombreConductor = "";
          let codigoConductor = "";
          let alquilerFecha = "";
          if (Object.keys(alquileres).length > 0) {
            for (i in alquileres) {
              alquiler = alquileres[i] ?? {};
              conductor = alquiler.conductor ?? {};
              nombreConductor = `${conductor.nombre ?? ""} ${conductor.apellido_paterno ?? ""}`;
              codigoConductor = conductor.cod_conductor ?? "";
              break;
            }
          }
          let turnos = data.turno_data ?? {};
          let htmlTurnoBtns = "";
          let turno = {};
          let btnAgregarHorario = "";
          let atributosData = "";
          if (contarTurnos > 0) {
            let auxBtn = "";
            let auxAttr = "";
            let auxSeparador = "";
            for (i in turnos) {
              turno = turnos[i];
              auxAttr = ` data-codigoturno="${turno.codigo ?? ""}" data-codigovehiculo="${data.cod_vehiculo ?? ""}"
              data-nombrevehiculo="${data.nom_vehiculo ?? ""}" data-codigohorario="${turno.horario_inicio ?? ""}"
              data-codigoconductor="${codigoConductor}" data-nombreconductor="${nombreConductor}" `;
              auxBtn = `<button type="button" ${auxAttr} class="btn btn-sm btn-cyan editar-turno"><i
              class="fa fa-edit"></i></button>`;
              if (htmlTurnoBtns == "") {
                auxSeparador = "";
              } else {
                auxSeparador = "|";
              }
              htmlTurnoBtns += `${auxSeparador} ${turno.horario_nombre ?? ""} ${auxBtn} <span
                class="text-black-50">${turno.fecha_programacion ?? ""} [${turno.hora_inicio ?? "*"} - ${turno.hora_fin ?? "*"}]</span>`;
            }
          }

          if (contarTurnos < 1) {
            atributosData = ` data-codigoturno="" data-codigovehiculo="${data.cod_vehiculo ?? ""}"
              data-nombrevehiculo="${data.nom_vehiculo ?? ""}" data-codigohorario=""
              data-codigoconductor="${codigoConductor}" data-nombreconductor="${nombreConductor}" `;
            btnAgregarHorario = `<button type="button" ${atributosData} class="btn btn-sm btn-cyan agregar-turno"><i
              class="fa fa-plus"></i></button>`;
            htmlTurnoBtns = btnAgregarHorario;
          }
          return htmlTurnoBtns;
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        data: function (data) {
          let alquileres = data.alquiler_data ?? {};
          let htmlAlquileres = "";
          let conductor = {};
          let nombreConductor = "";
          let alquilerFecha = "";
          let alquilerEntregaRadio = "";
          if (Object.keys(alquileres).length > 0) {
            for (i in alquileres) {
              alquiler = alquileres[i] ?? {};
              conductor = alquiler.conductor ?? {};
              nombreConductor = `${conductor.nombre ?? ""} ${conductor.apellido_paterno ?? ""}`;
              alquilerFecha = `[${alquiler.fecha_inicio ?? ""} - ${alquiler.fecha_prog_fin ?? "*"}]`;
              alquilerEntregaRadio = (alquiler.entrega_radio == true) ? "Con" : "Sin";
              htmlAlquileres += `${nombreConductor} | <span class="text-black-50">${alquilerFecha}</span>
              | <span>${alquilerEntregaRadio} radio</span>`;
            }
            return htmlAlquileres;
          }
          return "No hay ningun alquiler";
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        data: function (data) {
          return `${data.descripcion} <span class="text-black-50">${data.marca ?? ""}</span>`;
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "90",
        data: function (data) {
          return data.estado_vehiculo_text;
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "90",
        data: function (data) {
          return data.estado_alquilado_text;
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableTurnoVehiculo();
    }
  });

  tblTurnoVehiculo.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblTurnoVehiculo.DataTable().page.info();
    tblTurnoVehiculo.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-turno-vehiculo tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblTurnoVehiculo.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaTurnoVehiculoDatatable.map(
        (item) => `<th>${$("#lista-turno-vehiculo thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaTurnoVehiculoDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });


  // Modal
  $("#bs-selec-turno-vehiculo-modal-lg").on("show.bs.modal", function () {
    setTimeout(function () {
      fnTblEscogerHorarioTurno();
    }, 300);
  });

  $("#bs-selec-turno-vehiculo-modal-lg").on("hide.bs.modal", function () {
    fnTblEscHorarioConductorUncheck();
    setTimeout(function () {
      fnTblTurnoVehiculo();
      $campoBsSelectTurnoCodigo.val("");
      $campoBsSelectVehiculoCodigo.val("");
      $campoBsSelectConductorCodigo.val("");
      $campoBsSelectHorarioCodigo.val("");
      $idTurnoCampoFinalizar.prop("checked", false);
    }, 300);
  });

  fnTblTurnoVehiculo = function () {
    try {
      tblTurnoVehiculo.search("");
      tblTurnoVehiculo.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblTurnoVehiculo();

  $("#lista-turno-vehiculo tbody").on("click", ".agregar-turno", function () {
    const $auxBtn = $(this);
    const $auxModal = $("#bs-selec-turno-vehiculo-modal-lg");
    let codigoTurno = $auxBtn.data("codigoturno") ?? "";
    let codigoVehiculo = $auxBtn.data("codigovehiculo") ?? "";
    let nombreVehiculo = $auxBtn.data("nombrevehiculo") ?? "";
    let codigoHorario = $auxBtn.data("codigohorario") ?? "";
    let codigoConductor = $auxBtn.data("codigoconductor") ?? "";
    let nombreConductor = $auxBtn.data("nombreconductor") ?? "";
    let htmlTitulo = "Agregar turno conductor";
    let htmlDetalle = `Agregar nuevo Turno al vehiculo <span class="label label-megna">${nombreVehiculo}</span>
         con conductor <span class="label label-megna">${nombreConductor}</span>`;
    $auxModal.find(".modal-title").html(htmlTitulo);
    $auxModal.find(".detalle-operador").html(htmlDetalle);
    $campoBsSelectHorarioCodigo.val("");
    $campoBsSelectTurnoCodigo.val("");
    $campoBsSelectVehiculoCodigo.val(codigoVehiculo);
    $campoBsSelectConductorCodigo.val(codigoConductor);
    $auxModal.modal("show");
    $idTurnoCheckOpcFinalizar.hide();
  });

  $("#lista-turno-vehiculo tbody").on("click", ".editar-turno", function () {
    const $auxBtn = $(this);
    const $auxModal = $("#bs-selec-turno-vehiculo-modal-lg");
    let codigoTurno = $auxBtn.data("codigoturno") ?? "";
    const auxUrl = urlList.vehiculo.mantenerTurnoConductorDetail.replace("/0000/", `/${codigoTurno}/`);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    $.ajax({
      url: auxUrl,
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtn.prop("disabled", true);
      },
      success: function (resp) {
        let data = resp.data ?? {};
        let dataConductor = data.conductor_data ?? {};
        let nombreConductor = `${dataConductor.nombre ?? ""} ${dataConductor.apellido_paterno ?? ""}`;
        let dataVehiculo = data.vehiculo_data ?? {};
        let dataHorario = data.horario_data ?? {};
        let nombreVehiculo = `${dataVehiculo.nombre ?? ""}`;
        // ------------modificar para cargar desde back ---->>
        let htmlTitulo = "Modificar turno del conductor";
        let htmlDetalle = `Conductor actual <span class="label label-megna">${nombreConductor}</span>
            vehiculo <span class="label label-megna font-bold">${nombreVehiculo}</span> horario
            <span class="label label-megna">${dataHorario.nombre ?? ""}</span> fecha <span
            class="label label-megna">${data.fecha_programacion ?? ""}</span> <br>
            Para modificar seleccione <b>nuevo horario</b> o haga <b>check</b> en finalizar turno`;
        $auxModal.find(".modal-title").html(htmlTitulo);
        $auxModal.find(".detalle-operador").html(htmlDetalle);
        $campoBsSelectTurnoCodigo.val(codigoTurno);
        $campoBsSelectVehiculoCodigo.val(data.vehiculo ?? "");
        $campoBsSelectConductorCodigo.val(data.conductor ?? "");
        $campoBsSelectHorarioCodigo.val(data.horario_inicio ?? "");
        // -- datos de formulario
        $auxModal.modal("show");
        $idTurnoCheckOpcFinalizar.show();
        // ------------modificar para cargar desde back <<----
        $auxBtn.prop("disabled", false);
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego guardar";
        }
        swal.fire({
          title: "Alerta",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  });

  // ---------
  $btnTurnoConductorFinalizar.click(function () {
    if (!$idTurnoCampoFinalizar.is(":checked")) {
      $idTurnoCampoFinalizar.prop("checked", true);
    } else {
      $idTurnoCampoFinalizar.prop("checked", false);
    }
    return true;
  });
  // --------

  $btnFrmTurnoConductorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoTurno = $campoBsSelectTurnoCodigo.val();
    const codigoConductor = $campoBsSelectConductorCodigo.val() ?? "";
    const _data = $("#id_frm_select_turno :input").serializeArray();
    let auxUrl = "";
    let auxType = "PATCH";
    if (codigoTurno == "") {
      auxUrl = urlList.vehiculo.mantenerTurnoConductorList;
      auxType = "POST";
    } else {
      auxUrl = urlList.vehiculo.mantenerTurnoConductorDetail.replace("/0000/", `/${codigoTurno}/`);
    }
    if (codigoConductor == "") {
      swal.fire({
        title: "Alerta",
        text: "Seleccionar conductor",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    $.ajax({
      url: auxUrl,
      type: auxType,
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        $("#bs-selec-turno-vehiculo-modal-lg").modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego guardar";
        }
        swal.fire({
          title: "Alerta",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  });

  $btnFrmTurnoConductorCancelar.click(function () {
    $("#bs-selec-turno-vehiculo-modal-lg").modal("hide");
  });

});
