var fnTblProgTurnoOper = null;
const $campoBsSeleccionarOperador = $("#id_bs_agregar_operador_cod_operador");
$(document).ready(function () {
  const TURNO_HORARIO_01 = 0;
  const TURNO_HORARIO_02 = 1;
  const TURNO_HORARIO_03 = 2;

  const $campoBsSelectCodigoTurno = $("#id_bs_agregar_operador_cod_turno");
  const $campoBsSelectCodigoHorario = $("#id_bs_agregar_operador_cod_horario");
  const $campoBsSelectFecha = $("#id_bs_agregar_operador_fecha");

  const $btnSeleccionarOperadorGuardar = $("#btnSeleccionarOperadorGuardar");
  const $btnSeleccionarOperadorCancelar = $("#btnSeleccionarOperadorCancelar");

  const $tblProgTurnoOper = $("#lista-prog-turno-operadores");
  const $btnBuscarProgTurnoOper = $("#btn-buscar-prog-turno-operador");
  const arrayOcultarColumaProgTurnoOperDatatable = [];

  const TURNO_NO_CHECKET = `<i class="fa fa-square"></i>`;
  const TURNO_CHECKET = `<i class="fa fa-check"></i>`;

  const btnHtmlBuscar = `<span class="btn-label">${ICO_BUSCAR_2}</span>Buscar`;
  const btnHtmlBuscarLoad = `<span class="btn-label">${ICO_CARGANDO}</span>Buscar`;

  let dataHorarios = {};
  let dataHorariosKeys = {};
  let dataOperadores = {};

  function ocultarColumProgTurnoOperDatatable() {
    const filas = $("#lista-prog-turno-operadores tbody").find("tr").length;
    if (arrayOcultarColumaProgTurnoOperDatatable.length === 0) {
      $("#lista-prog-turno-operadores thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-prog-turno-operadores tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaProgTurnoOperDatatable.map((item) =>
        $("#lista-prog-turno-operadores thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaProgTurnoOperDatatable.map((item) => $("#lista-prog-turno-operadores tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  function fnDataViewOperadorHoarios(keyHorario, data) {
    let colorBtn = "btn-primary";
    if (keyHorario == TURNO_HORARIO_01) {
      colorBtn = "btn-primary";
    } else if (keyHorario == TURNO_HORARIO_02) {
      colorBtn = "btn-success";
    } else if (keyHorario == TURNO_HORARIO_03) {
      colorBtn = "btn-cyan";
    }
    let turnoOperador = (data[(dataHorariosKeys[keyHorario] ?? "")] ?? {});
    let codigo_turno = turnoOperador.turno_id ?? "";
    let codigo_operador = turnoOperador.operador ?? "";
    let operador = dataOperadores[codigo_operador] ?? {};
    let horario = (dataHorarios[(dataHorariosKeys[keyHorario] ?? "")] ?? {codigo: ""});
    // let estadoTurno = (turnoOperador.estado_turno_text) ? `| ${turnoOperador.estado_turno_text ?? ""}` : "";
    let estadoTurno = (turnoOperador.estado_turno_text) ? `${turnoOperador.estado_turno_text ?? ""}` : "";
    // let htmlView = `<span class="text-black-50">${horario.nom_horario} |
    //     ${horario.inicio_horario}-${horario.fin_horario} ${estadoTurno}</span>`;
    let htmlView = `<span class="text-black-50">${estadoTurno}</span>`;
    let frmData = ` data-codigoturno="${codigo_turno}" data-fecha="${data.fecha}" data-dia="${data.dia}"
           data-codigooperario="${codigo_operador}" data-codigohorario="${horario.codigo}"`;
    let frmBtn = "";
    if (codigo_turno == "") {
      frmBtn = `<button type="button" class="btn btn-sm ${colorBtn} agregar-operador"
                ${frmData}><i class="fa fa-plus"></i></button>`;
      return `${frmBtn} ${htmlView}`;
    }
    let permitirEditar = turnoOperador.editar ?? false;
    if (permitirEditar) {
      frmBtn = `<button type="button" class="btn btn-sm ${colorBtn} agregar-operador" ${frmData}><i
                    class="fa fa-edit"></i></button>`;
    }
    let htmlOperador = "";
    if (operador) {
      htmlOperador = `<span>${operador.nombre ?? ""} ${operador.apellido_paterno ?? ""}</span> |
                <span class="text-black-50">${operador.alias ?? ""}</span>`;
      if (["03", "04", "05"].includes(turnoOperador.estado_turno) && !permitirEditar) {
        let auxTurIni = (turnoOperador.hora_inicio ?? "").substring(0, 5);
        let auxTurFin = (turnoOperador.hora_inicio ?? "").substring(0, 5);
        frmBtn = `<span class="text-black-50">[${auxTurIni ?? "*"} - ${auxTurFin ?? "*"}]</span> |`;
      }
      return `${frmBtn} ${htmlOperador} | ${htmlView}`;
    }
    return `${frmBtn} ${htmlView}`;
  }

  const tblProgTurnoOper = $tblProgTurnoOper.DataTable({
    language: {url: urlList.dataTablesES},
    serverSide: true,
    destroy: true,
    deferRender: true,
    deferLoading: 0,
    searchDelay: 500,
    processing: true,
    searching: false,
    displayLength: 14,
    paging: true,
    lengthMenu: [7, 14, 21],
    pagingDelay: 500,
    responsive: true,
    order: [[2, 'asc']],
    ajax: {
      cache: false,
      url: urlList.turnoOperador.listTurnos,
      method: "get",
      dataType: "json",
      dataSrc: function (jsonData) {
        dataHorarios = jsonData.data_horarios;
        dataHorariosKeys = jsonData.data_horarios_keys;
        dataOperadores = jsonData.data_operarios;
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
          $btnBuscarProgTurnoOper.html(btnHtmlBuscar).prop("disabled", false);
        });
      }
    },
    columns: [
      {
        class: "text-center",
        orderable: false,
        searchable: false,
        data: function (data) {
          if (arrayOcultarColumaProgTurnoOperDatatable.length > 0) {
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
        className: "text-left",
        width: "60",
        searchable: false,
        orderable: false,
        data: function (data) {
          return data.fecha_view;
        }
      },
      {
        data: function (data) {
          let dia = data.dia ?? "";
          if (dia.length > 0) {
            return dia.substring(0, 1).toUpperCase() + dia.substring(1)
          }
          return "-";
        },
        width: "70",
        className: "text-center border-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return fnDataViewOperadorHoarios(TURNO_HORARIO_01, data);
        },
        className: "text-left border-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return fnDataViewOperadorHoarios(TURNO_HORARIO_02, data);
        },
        className: "text-left border-left",
        searchable: false,
        orderable: false
      },
      // {
      //   data: function (data) {
      //     let dia = data.dia ?? "";
      //     if (dia.length > 0) {
      //       return dia.substring(0, 1).toUpperCase() + dia.substring(1)
      //     }
      //     return "-";
      //   },
      //   width: "70",
      //   className: "text-center border-left",
      //   searchable: false,
      //   orderable: false
      // },
      {
        data: function (data) {
          return fnDataViewOperadorHoarios(TURNO_HORARIO_03, data);
        },
        className: "text-left border-left",
        searchable: false,
        orderable: false
      },
    ],
    drawCallback: function (settings) {
      ocultarColumProgTurnoOperDatatable();
    }
  });

  tblProgTurnoOper.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblProgTurnoOper.DataTable().page.info();
    tblProgTurnoOper.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  // Modal
  $("#bs-selec-operador-modal-lg").on("show.bs.modal", function () {
    setTimeout(function () {
      fnTblEscogerTurnoOpe();
    }, 300);
  });

  $("#bs-selec-operador-modal-lg").on("hide.bs.modal", function () {
    fnTblEscTurnoOpeUncheck();
    setTimeout(function () {
      fnTblProgTurnoOper();
      $campoBsSeleccionarOperador.val("");
      $campoBsSelectCodigoTurno.val("");
      $campoBsSelectCodigoHorario.val("");
      $campoBsSelectFecha.val("");
    }, 300);
  });

  $("#lista-prog-turno-operadores tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblProgTurnoOper.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaProgTurnoOperDatatable.map(
        (item) => `<th>${$("#lista-prog-turno-operadores thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaProgTurnoOperDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  $("#lista-prog-turno-operadores tbody").on("click", ".agregar-operador", function () {
    const $auxBtn = $(this);
    const $auxModal = $("#bs-selec-operador-modal-lg");
    let codigoOperario = $auxBtn.data("codigooperario") ?? "";
    let codigoTurno = $auxBtn.data("codigoturno") ?? "";
    let codigoHorario = $auxBtn.data("codigohorario") ?? "";
    let fecha = $auxBtn.data("fecha") ?? "";
    let diaNombre = $auxBtn.data("dia") ?? "";
    let dataHorario = dataHorarios[codigoHorario] ?? {};
    let nombreHorario = dataHorario.nom_horario ?? "-";
    let rangoHorario = `[${dataHorario.inicio_horario ?? "*"}-${dataHorario.fin_horario ?? "*"}]`;
    // ---------
    let htmlTitulo = "";
    let htmlDetalle = "";
    let operario = {}
    if (codigoOperario == "") {
      htmlTitulo = `Agregar operador | <b>${diaNombre.toUpperCase()} [${fecha}] - ${nombreHorario}</b>`;
      htmlDetalle = `Seleccionar al operador para la fecha
            <span class="badge badge-pill badge-cyan">${diaNombre.toUpperCase()}</span>
            <span class="badge badge-pill badge-cyan">${fecha}</span>
            en horario <span class="badge badge-pill badge-cyan">${nombreHorario} ${rangoHorario}</span>`;
    } else {
      htmlTitulo = `Modificar operador | <b>${diaNombre.toUpperCase()} [${fecha}] - ${nombreHorario}</b>`;
      operario = dataOperadores[codigoOperario];
      htmlDetalle = `Operador modificar
            <span class="badge badge-pill badge-cyan">${operario.nombre ?? ""}
            ${operario.apellido_paterno ?? ""} | ${operario.alias ?? ""}</span> para la fecha
            <span class="badge badge-pill badge-cyan">${diaNombre.toUpperCase()}</span>
            <span class="badge badge-pill badge-cyan">${fecha}</span>
            en horario <span class="badge badge-pill badge-cyan">${nombreHorario} ${rangoHorario}</span>`;
    }

    $auxModal.find(".modal-title").html(htmlTitulo);
    $auxModal.find(".detalle-operador").html(htmlDetalle);
    $campoBsSeleccionarOperador.val(codigoOperario);
    $campoBsSelectCodigoTurno.val(codigoTurno);
    $campoBsSelectCodigoHorario.val(codigoHorario);
    $campoBsSelectFecha.val(fecha);
    $auxModal.modal("show");
  });

  $btnSeleccionarOperadorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = $campoBsSelectCodigoTurno.val();
    const codigoOperador = $campoBsSeleccionarOperador.val();
    const _data = $("#id_frm_agregar_operador :input").serializeArray();
    let auxUrl = "";
    let auxType = "PATCH";
    if (numeroId == "") {
      auxUrl = urlList.turnoOperador.listTurnos;
      auxType = "POST";
    } else {
      auxUrl = urlList.turnoOperador.detalleTurno.replace("/0000/", `/${numeroId}/`);
    }
    if (codigoOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "Seleccionar operador",
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
        $("#bs-selec-operador-modal-lg").modal("hide");
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
  $btnSeleccionarOperadorCancelar.click(function () {
    $("#bs-selec-operador-modal-lg").modal("hide");
  });


  // Modal

  const $campoProgramOpeFecha = $("#id_program_ope_fecha");
  const $modalGenerarProgramacionoperador = $("#bs-generar-programacion-operadores-modal-lg");
  const $btnAgregarGenerarProgramacionOperador = $("#btnAgregarGenerarProgramacionOperador");
  const $btnProgramacionOperadoresGenerar = $("#btnProgramacionOperadoresGenerar");
  const $btnProgramacionOperadoresCancelar = $("#btnProgramacionOperadoresCancelar");

  // $("#bs-generar-programacion-operadores-modal-lg").on("show.bs.modal", function () {
  //   setTimeout(function () {
  //     $campoProgramOpeFecha.val("");
  //   }, 300);
  // });

  $("#bs-generar-programacion-operadores-modal-lg").on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblProgTurnoOper();
      $campoProgramOpeFecha.val("");
    }, 300);
  });

  $btnAgregarGenerarProgramacionOperador.click(function () {
    $modalGenerarProgramacionoperador.modal("show");
  });

  $btnProgramacionOperadoresGenerar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = "0000";
    const fecha = $campoProgramOpeFecha.val();
    const _data = $("#id_frm_programacion_operadores :input").serializeArray();
    const auxUrl = urlList.turnoOperador.generarProgramOperadores.replace("/0000/", `/${numeroId}/`);
    if (fecha == "") {
      swal.fire({
        title: "Alerta",
        text: "Seleccionar la fecha",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    $.ajax({
      url: auxUrl,
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) { // TODO mejorar el mensaje, no se muestra registros con error (falta implementar)
        $auxBtnExce.prop("disabled", false);
        swal.fire({
          title: "Alerta",
          text: "Se generó correctamente",
          type: "success",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
        $modalGenerarProgramacionoperador.modal("hide");
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

  $btnProgramacionOperadoresCancelar.click(function () {
    $modalGenerarProgramacionoperador.modal("hide");
  });

  fnTblProgTurnoOper = function () {
    try {
      tblProgTurnoOper.search("");
      tblProgTurnoOper.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblProgTurnoOper();

});
