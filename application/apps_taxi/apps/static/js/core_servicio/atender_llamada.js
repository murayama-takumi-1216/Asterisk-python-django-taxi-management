const $campoAtenderLlamdaServicioTurno = $("#id_servicio_turno");
var idCodigoTurnoConductor = "";
$(document).ready(function () {
  const TIPO_LLENAR_CAMPOS_LLAMADA = "modificar";
  const TIPO_LLENAR_CAMPOS_MODIFICAR = "llamada";
  const TIPO_LLENAR_CAMPOS_NUEVO = "nuevo";
  // ------------
  const FINALIZAR_NO_CHECKET = `<i class="far fa-square"></i> Finalizar`;
  const FINALIZAR_CHECKET = `<i class="far fa-check-square"></i> Finalizar`;
  const $campoFinServCheckFinalizar = $("#id_fin_serv_checkfinalizar");
  const CANCELAR_NO_CHECKET = `<i class="far fa-square"></i> Cancelar`;
  const CANCELAR_CHECKET = `<i class="far fa-check-square"></i> Cancelar`;
  const $campoFinServCheckCancelar = $("#id_fin_serv_checkcancelar");
  // --------------
  const $campoCodigoLlamada = $("#id_codigo_llamada");
  const $campoClienteCodigo = $("#id_cliente_codigo");
  const $campoServicioCodigo = $("#id_codigo_servicio");
  const $campoClienteNombres = $("#id_cliente_nombres");
  const $campoClienteApellidoPaterno = $("#id_cliente_apellido_paterno");
  const $campoClienteApellidoMaterno = $("#id_cliente_apellido_materno");
  const $campoClienteTelefono = $("#id_cliente_telefono");
  const $campoClienteGenero = $("#id_cliente_genero");
  const $campoClienteCorreo = $("#id_cliente_correo");
  const $campoServicioRefOrigen = $("#id_servicio_ref_origen");
  const $campoServicioRefDestino = $("#id_servicio_ref_destino");
  const $campoServicioFechaProg = $("#id_servicio_fecha_prog");
  const $campoServicioHoraProg = $("#id_servicio_hora_prog");
  const $campoServicioPasajeros = $("#id_servicio_pasajeros");
  const $campoServicioMonto = $("#id_servicio_monto");
  const $campoServicioObservacion = $("#id_servicio_observacion");
  // ------ finalizar servicio
  const $campoFinServCodigoServicio = $("#id_fin_serv_codigo_servicio");
  const $campoFinServCodigoLlamada = $("#id_fin_serv_codigo_llamada");
  const $campoFinServClienteCodigo = $("#id_fin_serv_cliente_codigo");
  const $campoFinServClienteNombres = $("#id_fin_serv_cliente_nombres");
  const $campoFinServClienteApellidoPaterno = $("#id_fin_serv_cliente_apellido_paterno");
  const $campoFinServClienteApellidoMaterno = $("#id_fin_serv_cliente_apellido_materno");
  const $campoFinServClienteTelefono = $("#id_fin_serv_cliente_telefono");
  const $campoFinServClienteGenero = $("#id_fin_serv_cliente_genero");
  const $campoFinServClienteCorreo = $("#id_fin_serv_cliente_correo");
  const $campoFinServServicioRefOrigen = $("#id_fin_serv_servicio_ref_origen");
  const $campoFinServServicioRefDestino = $("#id_fin_serv_servicio_ref_destino");
  const $campoFinServServicioFechaProg = $("#id_fin_serv_servicio_fecha_prog");
  const $campoFinServServicioHoraProg = $("#id_fin_serv_servicio_hora_prog");
  const $campoFinServServicioPasajeros = $("#id_fin_serv_servicio_pasajeros");
  const $campoFinServServicioMonto = $("#id_fin_serv_servicio_monto");
  const $campoFinServServicioObservacion = $("#id_fin_serv_servicio_observacion");
  const $campoFinServServicioHoraInicio = $("#id_fin_serv_hora_inicio");
  const $campoFinServServicioHoraFin = $("#id_fin_serv_hora_fin");

  const $btnAgregarServicioGuardar = $("#btnAgregarServicioGuardar");
  const $btnAgregarServicioCancelar = $("#btnAgregarServicioCancelar");

  const $btnAtenderLlamadaGuardar = $("#btnAtenderLlamadaGuardar");
  const $btnAtenderLlamadaCancelar = $("#btnAtenderLlamadaCancelar");

  const $btnFinalizarServicioGuardar = $("#btnFinalizarServicioGuardar");
  const $btnFinalizarServicioCancelar = $("#btnFinalizarServicioCancelar");

  $("#lista-llamada-cliente").on("click", ".llamadas-contestar", function () {
    const $auxBtnLlamadaCliente = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = $auxBtnLlamadaCliente.data("numero_id");
    $.ajax({
      url: urlList.llamada.contestarLlamada.replace("0000", numeroId),
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        fnLlamadaClienteLlenarCampos(resp.data, resp.choices, resp.fecha_actual, TIPO_LLENAR_CAMPOS_LLAMADA);
        fnCargarSugerenciaRutas(resp.data_sugerencia ?? "");
        $("#bs-nuevo-servicio-modal-lg").modal("show");
        $("#bs-nuevo-servicio-modal-lg .modal-title").html("Crear nuevo servicio");
        $campoAtenderLlamdaServicioTurno.val("");
        $("#id_servicio_turno_anterior").val("");
        $("#id_servicio_mensaje_modificar").hide();
        $("#id_servicio_mensaje_modificar .servicio_mensaje").html("");
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al contestar la llamada";
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

  $(".container-fluid").on("click", "#bntAgregarServicio", function () {
    const $auxBtnLlamadaCliente = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = $auxBtnLlamadaCliente.data("numero_id");

    $.ajax({
      url: urlList.llamada.contestarLlamada.replace("0000", numeroId),
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        fnNuevoServicioLlenarCampos(resp.data, resp.choices, resp.fecha_actual, TIPO_LLENAR_CAMPOS_NUEVO);
        $("#bs-agregar-servicio-modal-lg").modal("show");
        $("#bs-agregar-servicio-modal-lg .modal-title").html("Crear nuevo servicio");
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al contestar la llamada";
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

  $("#lista-llamada-cliente").on("click", ".llamadas-llamar", function () {
    const $auxBtnLlamadaCliente = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = $auxBtnLlamadaCliente.data("numero_id");
    $.ajax({
      url: urlList.llamada.listLlamadaClientBackCall.replace("0000", numeroId),
      type: "PATCH",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
      },
      success: function (resp) {
        swal.fire({
          title: "Alerta",
          text: "Se esta realizando la llamada al cliente, timbrará su extención",
          type: "success",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
        $auxBtnLlamadaCliente.prop("disabled", false);
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al llamar";
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

  $("#lista-asignar-taxi").on("click", ".asignar-taxi", function () {
    const $auxBtnLlamadaCliente = $(this);
    // const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const servicioId = $auxBtnLlamadaCliente.data("codigoservicio");
    fnModificarDatosServicioAgregarConductor($auxBtnLlamadaCliente, servicioId);
    // $.ajax({
    //   url: urlList.llamada.modificarAtencion.replace("0000", servicioId),
    //   type: "GET",
    //   dataType: "json",
    //   headers: {"X-CSRFToken": csrfToken},
    //   beforeSend: function () {
    //     $auxBtnLlamadaCliente.prop("disabled", true);
    //     $campoServicioCodigo.val("");
    //   },
    //   success: function (resp) {
    //     $auxBtnLlamadaCliente.prop("disabled", false);
    //     fnLlamadaClienteLlenarCampos(resp.data, resp.choices, TIPO_LLENAR_CAMPOS_MODIFICAR);
    //     fnCargarSugerenciaRutas(resp.data_sugerencia ?? "");
    //     $("#bs-nuevo-servicio-modal-lg").modal("show");
    //     $("#bs-nuevo-servicio-modal-lg .modal-title").html("Asignar taxi al servicio");
    //     $campoAtenderLlamdaServicioTurno.val("");
    //     $("#id_servicio_turno_anterior").val("");
    //     $("#id_servicio_mensaje_modificar").hide();
    //     $("#id_servicio_mensaje_modificar .servicio_mensaje").html("");
    //   },
    //   error: function (request, status, data) {
    //     $auxBtnLlamadaCliente.prop("disabled", false);
    //     let mensaje = "";
    //     try {
    //       mensaje = request.responseJSON.data_ws.error.message;
    //     } catch (e) {
    //       mensaje = "Hubo inconvenientes al asignar taxi";
    //     }
    //     swal.fire({
    //       title: "Alerta",
    //       text: mensaje,
    //       type: "warning",
    //       showConfirmButton: true, confirmButtonText: "Cerrar",
    //     });
    //   }
    // });
  });

  function fnModificarDatosServicioAgregarConductor($auxBtnLlamadaCliente, servicioId) {
    // const $btnAbrir = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    // let servicioId = $btnAbrir.data("codigoservicio");
    // if (servicioIdValue != "") {
    //   servicioId = servicioIdValue;
    // }
    $.ajax({
      url: urlList.llamada.modificarAtencion.replace("0000", servicioId),
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
        $campoServicioCodigo.val("");
      },
      success: function (resp) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        fnLlamadaClienteLlenarCampos(resp.data, resp.choices, resp.fecha_actual, TIPO_LLENAR_CAMPOS_MODIFICAR);
        fnCargarSugerenciaRutas(resp.data_sugerencia ?? "");
        $("#bs-nuevo-servicio-modal-lg").modal("show");
        $("#bs-nuevo-servicio-modal-lg .modal-title").html("Asignar taxi al servicio");
        $campoAtenderLlamdaServicioTurno.val("");
        $("#id_servicio_turno_anterior").val("");
        $("#id_servicio_mensaje_modificar").hide();
        $("#id_servicio_mensaje_modificar .servicio_mensaje").html("");
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al asignar taxi";
        }
        swal.fire({
          title: "Alerta",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }

  $("#lista-turnos-escoger-01").on("click", ".detalle-itinerario-conductor", function () {
    const $btnShow = $(this);
    fnShowDetalleItinerarioConductor($btnShow);
  });
  $("#lista-turnos-escoger-02").on("click", ".detalle-itinerario-conductor", function () {
    const $btnShow = $(this);
    fnShowDetalleItinerarioConductor($btnShow);
  });

  $btnAgregarServicioGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    let llamadaId = "0";
    // -------- llenar datos por defecto - inicio
    $("#id_ns_cliente_nombres").val("x0");
    $("#id_ns_cliente_apellido_paterno").val("x1");
    $("#id_ns_cliente_apellido_materno").val("x2");
    // -------- llenar datos por defecto - fin
    const _data = $("#id_frm_agregar_nuevo_servicio :input").serializeArray();
    _data.push({"name": "accion", "value": "agregar"});
    const urlTegistrarDatos = urlList.llamada.agregarServicio.replace("/0000/", `/${llamadaId}/`);
    $.ajax({
      url: urlTegistrarDatos,
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        $("#bs-agregar-servicio-modal-lg").modal("hide");
        // ----------------------------
        setTimeout(function () {
          fnTblAsignarTaxi();
          let dateNow = new Date();
          let horaMinActual = `${dateNow.getHours().toString().padStart(2, "0")}:${dateNow.getMinutes().toString().padStart(2, "0")}`;
          $("#id_ns_cliente_codigo").val("");
          $("#id_ns_cliente_nombres").val("");
          $("#id_ns_cliente_apellido_paterno").val("");
          $("#id_ns_cliente_apellido_materno").val("");
          $("#id_ns_cliente_telefono").val("");
          $("#id_ns_cliente_genero").val("");
          $("#id_ns_servicio_ref_origen").val("");
          $("#id_ns_servicio_ref_destino").val("");
          $("#id_ns_servicio_hora_prog").val(horaMinActual);
          $("#id_ns_servicio_monto").val("8.00");
          let servicioId = (((resp ?? {}).servicio ?? {}).data ?? {}).id;
          fnModificarDatosServicioAgregarConductor($auxBtnExce, servicioId);
        }, 450);


      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        let detail = {};
        let errors = [];
        let errorsDetail = [];
        let mensajeHtml = "";
        try {
          detail = request.responseJSON.detail ?? {};
          mensaje = (detail.cliente ?? {}).message ?? (detail.servicio ?? {}).message ?? "";
          mensaje2 = detail.message ?? "";
          errors = (detail.cliente ?? {}).errors ?? (detail.servicio ?? {}).errors ?? {};
          if (Object.keys(errors).length > 0 && mensaje.length > 0) {
            for (let keyItem in errors) {
              errorsDetail.push(`
                <b>${keyItem.toString().replace("_", " ")}: </b>
                ${errors[keyItem].join(", ")}`);
            }
            mensajeHtml = `${mensaje} <br> ${errorsDetail.join("<br>")}`;
          } else if (mensaje.length > 0) {
            mensajeHtml = mensaje;
          } else if (mensaje2.length > 0) {
            mensajeHtml = mensaje2;
          }
        } catch (e) {
          mensaje = "No se llego guardar registro";
        }
        swal.fire({
          title: "Alerta",
          html: `${mensaje} <br> ${errorsDetail.join("<br>")}`,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  });
  $btnAgregarServicioCancelar.click(function () {
    $("#bs-agregar-servicio-modal-lg").modal("hide");
  });

  $btnAtenderLlamadaGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    let numeroId = $campoCodigoLlamada.val();
    const _data = $("#id_frm_atender_llamada_nuevo :input").serializeArray();
    let urlTegistrarDatos = urlList.llamada.registrarLlamada.replace("/0000/", `/${numeroId}/`);
    if ($campoServicioCodigo.val() != "") {
      numeroId = $campoServicioCodigo.val();
      urlTegistrarDatos = urlList.llamada.modificarAtencion.replace("/0000/", `/${numeroId}/`);
    }
    $.ajax({
      url: urlTegistrarDatos,
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        $("#bs-nuevo-servicio-modal-lg").modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        let detail = {};
        let errors = [];
        let errorsDetail = [];
        try {
          detail = request.responseJSON.detail ?? {};
          mensaje = (detail.cliente ?? {}).message ?? (detail.servicio ?? {}).message ?? "";
          errors = (detail.cliente ?? {}).errors ?? (detail.servicio ?? {}).errors ?? {};

          for (let keyItem in errors) {
            errorsDetail.push(`
                <b>${keyItem.toString().replace("_", " ")}: </b>
                ${errors[keyItem].join(", ")}`);
          }
        } catch (e) {
          mensaje = "No se llego guardar registro";
        }
        swal.fire({
          title: "Alerta",
          html: `${mensaje} <br> ${errorsDetail.join("<br>")}`,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  });
  $btnAtenderLlamadaCancelar.click(function () {
    $("#bs-nuevo-servicio-modal-lg").modal("hide");
  });

  // Finalizar servicio de atencion
  function fnFinalizarAtencionClienteAtendido($btnAction) {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const servicioId = $btnAction.data("codigoservicio");
    const _data = [];
    _data.push({name: "accion", value: "atendido"});
    $.ajax({
      url: urlList.servicio.finalizarDetalle.replace("/0000/", `/${servicioId}/`),
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $btnAction.prop("disabled", true);
      },
      success: function (resp) {
        $btnAction.prop("disabled", false);
        fnTblPendienteAtencion();
      },
      error: function (request, status, data) {
        $btnAction.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego guardar la llamada";
        }
        swal.fire({
          title: "Alerta",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }

  $("#lista-pendientes-en-atencion").on("click", ".finalizar-servicio-atendido", function () {
    const $btnAction = $(this);
    $btnAction.prop("disabled", true);
    const nombreVehiculo = $btnAction.data("nombrevehiculo");
    const nombreConductor = $btnAction.data("nombreconductor");
    let htmlText = `EL conductor <span class="badge badge-pill table-info font-bold">${nombreConductor}</span>
        con el vehículo <span class="badge badge-pill table-info font-bold">${nombreVehiculo}</span>
        finalizó el servicio al cliente correctamente. <br> ¿Desea finalizar atención?`
    swal.fire({
      title: "Se realizó el servicio",
      html: htmlText,
      type: "success",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonText: "Confirmar",
      cancelButtonText: "Cancelar"
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnFinalizarAtencionClienteAtendido($btnAction);
        return true;
      }
      $btnAction.prop("disabled", false);
    });
  });

  function fnFinalizarAtencionClienteClienteCancela($btnAction) {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const servicioId = $btnAction.data("codigoservicio");
    const _data = [];
    _data.push({name: "accion", value: "cancelcli"});
    $.ajax({
      url: urlList.servicio.finalizarDetalle.replace("/0000/", `/${servicioId}/`),
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $btnAction.prop("disabled", true);
      },
      success: function (resp) {
        $btnAction.prop("disabled", false);
        fnTblPendienteAtencion();
      },
      error: function (request, status, data) {
        $btnAction.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego guardar la llamada";
        }
        swal.fire({
          title: "Alerta",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }

  $("#lista-pendientes-en-atencion").on("click", ".finalizar-servicio-cancelcli", function () {
    const $btnAction = $(this);
    $btnAction.prop("disabled", true);
    const nombreVehiculo = $btnAction.data("nombrevehiculo");
    const nombreConductor = $btnAction.data("nombreconductor");
    let htmlText = `EL conductor <span class="badge badge-pill table-primary font-bold">${nombreConductor}</span>
        con el vehículo <span class="badge badge-pill table-primary font-bold">${nombreVehiculo}</span>
        indicó que el cliente canceló el servicio. <br> ¿Desea cancelar el servicio?`
    swal.fire({
      title: "El Cliente canceló el Servicio",
      html: htmlText,
      type: "warning",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonText: "Confirmar",
      cancelButtonText: "Cancelar"
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnFinalizarAtencionClienteClienteCancela($btnAction);
        return true;
      }
      $btnAction.prop("disabled", false);
    });
  });

  $("#lista-pendientes-en-atencion").on("click", ".finalizar-servicio-modificar", function () {
    const $auxBtnLlamadaCliente = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const servicioId = $auxBtnLlamadaCliente.data("codigoservicio");
    $.ajax({
      url: urlList.llamada.modificarAtencion.replace("0000", servicioId),
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
        $campoServicioCodigo.val("");
      },
      success: function (resp) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        idCodigoTurnoConductor = (resp.data ?? {}).turno_conductor ?? "";
        fnLlamadaClienteLlenarCampos(resp.data, resp.choices, resp.fecha_actual, TIPO_LLENAR_CAMPOS_MODIFICAR);
        fnCargarSugerenciaRutas(resp.data_sugerencia ?? "");
        $("#bs-nuevo-servicio-modal-lg").modal("show");
        $("#bs-nuevo-servicio-modal-lg .modal-title").html("Modificar servicio");
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al asignar taxi";
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

  $btnFinalizarServicioGuardar.click(function () {
    if (true) { // TODO opcion deshabilitada (deberia borrarse)
      $("#bs-finalizar-servicio-modal-lg").modal("hide");
      return true;
    }
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const numeroId = $campoFinServCodigoServicio.val();
    const _data = $("#id_frm_finalizar_servicio :input").serializeArray();
    _data.push({name: "accion", value: "nada"})
    $.ajax({
      url: urlList.servicio.finalizarDetalle.replace("/0000/", `/${numeroId}/`),
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        $("#bs-finalizar-servicio-modal-lg").modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego guardar la llamada";
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
  $btnFinalizarServicioCancelar.click(function () {
    $("#bs-finalizar-servicio-modal-lg").modal("hide");
  });


  $("#lista-pendientes-en-atencion").on("click", ".detalle-servicio", function () {
    const $auxBtnLlamadaCliente = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const servicioId = $auxBtnLlamadaCliente.data("codigoservicio");
    $.ajax({
      url: urlList.servicio.finalizarAtencion.replace("/0000/", `/${servicioId}/`),
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnLlamadaCliente.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        fnFinalizarServicioLlenarCampos(resp.data, resp.choices);
        $("#bs-finalizar-servicio-modal-lg").modal("show");
      },
      error: function (request, status, data) {
        $auxBtnLlamadaCliente.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "Hubo inconvenientes al cargar datos del servicio";
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

  // Modal
  $("#bs-nuevo-servicio-modal-lg").on("show.bs.modal", function () {
    varTblEscogerTurno01_turnoAutomatico = 1;
    fnRefreshLlamadasCliente("NO");
    $("#detalle-lista-servicios-conductor").hide();
    setTimeout(function () {
      fnTblEscogerTurno01();
    }, 300);
  });

  $("#bs-nuevo-servicio-modal-lg").on("hide.bs.modal", function () {
    $campoAtenderLlamdaServicioTurno.val("");
    varTblEscogerTurno01_turnoAutomatico = 0;
    fnTblEscTurnoUncheck();
    fnRefreshLlamadasCliente("SI");
    $campoAtenderLlamdaServicioTurno.val("");
    $("#id_servicio_turno_anterior").val("");
    $("#id_servicio_mensaje_modificar .servicio_mensaje").html("");
    $("#id_servicio_mensaje_modificar").hide();
    setTimeout(function () {
      fnTblPendienteAtencion();
      fnTblAsignarTaxi();
      fnTblLlamadaCliente();
      $("#mostrarServicioFrecuentes").html("");
    }, 300);
  });

  $("#bs-finalizar-servicio-modal-lg").on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblPendienteAtencion();
      // ------ desactivar boton ini
      $campoFinServCheckFinalizar.val("");
      $("#btnFinServCheckFinalizar").removeClass("btn-cyan").addClass("btn-secondary").html(FINALIZAR_NO_CHECKET);
      $campoFinServCheckCancelar.val("");
      $("#btnFinServCheckCancelar").removeClass("btn-cyan").addClass("btn-secondary").html(CANCELAR_NO_CHECKET);
      // ------ desactivar boton fin
    }, 300);
  });

  $("#bs-turno-conductor-modal-lg").on("show.bs.modal", function () {
    $("#detalle-servicios-turnoconductor").hide();
    setTimeout(function () {
      fnTblTurnoConductor01();
    }, 300);
  });

  $("#bs-turno-conductor-modal-lg").on("hide.bs.modal", function () {
    $("#bntTurnoConductoresView").prop("disabled", false);
  });

  function fnNuevoServicioLlenarCampos(data, choices, serverFechaActual, tipo = "llamada") {
    let fechArray = serverFechaActual.date.split("-");
    let horArray = serverFechaActual.time.split(":");
    let dateNow = new Date();
    let fechaActual = `${fechArray[0].toString()}-${(fechArray[1]).toString().padStart(2, "0")}-${(fechArray[2]).toString().padStart(2, "0")}`;
    let fechaActual2 = `${dateNow.getFullYear()}-${(dateNow.getMonth() + 1).toString().padStart(2, "0")}-${(dateNow.getDay() + 1).toString().padStart(2, "0")}`;
    let horaMinActual = `${(horArray[0]).toString().padStart(2, "0")}:${(horArray[1]).toString().padStart(2, "0")}`;
    let horaMinActual2 = `${dateNow.getHours().toString().padStart(2, "0")}:${dateNow.getMinutes().toString().padStart(2, "0")}`;
    let _html = "";
    for (let i in choices.genero) {
      _html += `<option value="${i}">${choices.genero[i]}</option>`
    }
    $campoCodigoLlamada.val("");
    $campoServicioCodigo.val("");
    let nombreCliente = (data.cliente_data ?? {}).nombre ?? (data.callerid_name ?? "");
    $("#id_ns_cliente_genero").html(_html);
    $("#id_ns_cliente_codigo").val((data.cliente_data ?? {}).codigo ?? "");
    $("#id_ns_cliente_nombres").val(nombreCliente);
    $("#id_ns_cliente_apellido_paterno").val((data.cliente_data ?? {}).apellido_paterno ?? "");
    $("#id_ns_cliente_apellido_materno").val((data.cliente_data ?? {}).apellido_materno ?? "");
    $("#id_ns_cliente_telefono").val((data.cliente_data ?? {}).telefono ?? (data.numero ?? ""));
    $("#id_ns_cliente_genero").val((data.cliente_data ?? {}).genero ?? "");
    $("#id_ns_servicio_ref_origen").val(data.referencia_origen ?? "");
    $("#id_ns_servicio_ref_destino").val(data.referencia_destino ?? "");
    $("#id_ns_servicio_hora_prog").val(data.hora_programada ?? horaMinActual);
    $("#id_ns_servicio_monto").val(data.monto_servicio ?? "8.00");
  }

  function fnLlamadaClienteLlenarCampos(data, choices, serverFechaActual, tipo = "llamada") {
    let fechArray = serverFechaActual.date.split("-");
    let horArray = serverFechaActual.time.split(":");
    let dateNow = new Date();
    let fechaActual = `${fechArray[0].toString()}-${(fechArray[1]).toString().padStart(2, "0")}-${(fechArray[2]).toString().padStart(2, "0")}`;
    let fechaActual2 = `${dateNow.getFullYear()}-${(dateNow.getMonth() + 1).toString().padStart(2, "0")}-${(dateNow.getDay() + 1).toString().padStart(2, "0")}`;
    let horaMinActual = `${(horArray[0]).toString().padStart(2, "0")}:${(horArray[1]).toString().padStart(2, "0")}`;
    let horaMinActual2 = `${dateNow.getHours().toString().padStart(2, "0")}:${dateNow.getMinutes().toString().padStart(2, "0")}`;
    let _html = "";
    for (let i in choices.genero) {
      _html += `<option value="${i}">${choices.genero[i]}</option>`
    }
    if (tipo === TIPO_LLENAR_CAMPOS_LLAMADA) {
      $campoCodigoLlamada.val(data.id ?? "");
      $campoServicioCodigo.val("");
    } else if (tipo === TIPO_LLENAR_CAMPOS_MODIFICAR) {
      $campoCodigoLlamada.val("");
      $campoServicioCodigo.val(data.id ?? "");
    } else if (tipo === TIPO_LLENAR_CAMPOS_NUEVO) {
      $campoCodigoLlamada.val("");
      $campoServicioCodigo.val("");
    }
    let nombreCliente = (data.cliente_data ?? {}).nombre ?? (data.callerid_name ?? "");
    if (nombreCliente == "x0") {
      nombreCliente = "";
    }

    let apellidoPaterno = (data.cliente_data ?? {}).apellido_paterno ?? "";
    if (apellidoPaterno == "x1") {
      apellidoPaterno = "";
    }

    let apellidoMaterno = (data.cliente_data ?? {}).apellido_materno ?? "";
    if (apellidoMaterno == "x2") {
      apellidoMaterno = "";
    }

    $campoClienteGenero.html(_html);
    $campoClienteCodigo.val((data.cliente_data ?? {}).codigo ?? "");
    $campoClienteNombres.val(nombreCliente);
    $campoClienteApellidoPaterno.val(apellidoPaterno);
    $campoClienteApellidoMaterno.val(apellidoMaterno);
    $campoClienteTelefono.val((data.cliente_data ?? {}).telefono ?? (data.numero ?? ""));
    $campoClienteGenero.val((data.cliente_data ?? {}).genero ?? "");
    $campoClienteCorreo.val((data.cliente_data ?? {}).correo ?? "");
    $campoServicioRefOrigen.val(data.referencia_origen ?? "");
    $campoServicioRefDestino.val(data.referencia_destino ?? "");
    $campoServicioFechaProg.val(data.fecha_programada ?? fechaActual);
    $campoServicioHoraProg.val(data.hora_programada ?? horaMinActual);
    $campoServicioPasajeros.val(data.pasajeros ?? "");
    $campoServicioMonto.val(data.monto_servicio ?? "8.00");
    $campoServicioObservacion.val(data.observacion_registro ?? "");
    if (idCodigoTurnoConductor != "") {
      let nombresConductor = (data.turno_cond_data ?? {}).conductor_data ?? {};
      let nombreVehiculo = (data.turno_cond_data ?? {}).vehiculo_data ?? {};
      $campoAtenderLlamdaServicioTurno.val(idCodigoTurnoConductor);
      $("#id_servicio_turno_anterior").val(idCodigoTurnoConductor);
      $("#id_servicio_mensaje_modificar .servicio_mensaje").html(`
        <b class="bg-cyan rounded text-white pl-1 pr-1">Guardado</b>&nbsp;&nbsp;
        <b>Vehiculo:</b> <span class="text-uppercase">${nombreVehiculo.nombre ?? ""}</span> |
        <b>Conductor:</b> <span class="text-uppercase">${nombresConductor.nombre ?? ""} ${nombresConductor.apellido_paterno ?? ""}</span>
        `);
      $("#id_servicio_mensaje_modificar").show();
    } else {
      $campoAtenderLlamdaServicioTurno.val("");
      $("#id_servicio_turno_anterior").val("");
      $("#id_servicio_mensaje_modificar").hide();
      $("#id_servicio_mensaje_modificar .servicio_mensaje").html("");
    }
  }

  function fnCargarSugerenciaRutas(data = "") {
    let html = "";
    let dataJson = [];
    html += `<div>`;
    if (data.length > 4) {
      dataJson = JSON.parse(data) ?? [];
      dataJson.forEach((item, key) => {
        html += `<p class="mt-1 mb-0">
        <label class="label label-success btnAsignarData" data-item="${(key + 1)}">Asignar</label>
        <span id="cargaDataOrigen${(key + 1)}">${item.origen}</span>
        <i class="fa fa-arrow-right text-success"> </i> <span id="cargaDataDestino${(key + 1)}">${item.destino}</span>
        <label class="label label-megna" >${item.subtotal}</label>
        </p>`;
      });
    } else {
      html += `<p>No hay información para mostrar</p>`;
    }
    html += "</div>";
    $("#mostrarServicioFrecuentes").html(html);
  }

  $("#mostrarServicioFrecuentes").on("click", ".btnAsignarData", function () {
    const $btnCargar = $(this);
    const item = $btnCargar.data("item");
    const dataOrigen = $(`#cargaDataOrigen${item}`).text() ?? "";
    const dataDestino = $(`#cargaDataDestino${item}`).text() ?? "";
    $campoServicioRefOrigen.val(dataOrigen);
    $campoServicioRefDestino.val(dataDestino);

  });

  function fnShowDetalleItinerarioConductor($btnShow = null) {
    const $leyendaForm = $("#detalle-lista-servicios-conductor-leyenda");
    const tituloLeyenda = "DETALLE SERVICIOS DEL CONDUCTOR - TURNO";
    const $campoDato = $("#id_show_turno_dataid");
    if (!($campoDato.val()) || $btnShow.data("codigoturno").toString() !== $campoDato.val()) {
      $("#detalle-lista-servicios-conductor").show();
      $campoDato.val($btnShow.data("codigoturno"));
      $leyendaForm.html(`${tituloLeyenda}: ${$btnShow.data("nombre") ?? ""} / ${$btnShow.data("vehiculo") ?? ""}`);
      fnTblServiciosConductor();
    } else {
      $("#detalle-lista-servicios-conductor").hide();
      $campoDato.val("");
      $leyendaForm.html(`${tituloLeyenda}`);
    }
  }

  function fnFinalizarServicioLlenarCampos(data, choices) {
    let dateNow = new Date();
    let horaMinActual = `${dateNow.getHours().toString().padStart(2, "0")}:${dateNow.getMinutes().toString().padStart(2, "0")}`;
    $campoFinServCodigoServicio.val(data.id ?? "");
    $campoFinServClienteCodigo.val((data.cliente_data ?? {}).codigo ?? "");
    $campoFinServClienteNombres.val((data.cliente_data ?? {}).nombre ?? "");
    $campoFinServClienteApellidoPaterno.val((data.cliente_data ?? {}).apellido_paterno ?? "");
    $campoFinServClienteApellidoMaterno.val((data.cliente_data ?? {}).apellido_materno ?? "");
    $campoFinServClienteTelefono.val((data.cliente_data ?? {}).telefono ?? (data.numero ?? ""));
    $campoFinServClienteGenero.val((data.cliente_data ?? {}).genero ?? "");
    $campoFinServClienteCorreo.val((data.cliente_data ?? {}).correo ?? "");
    $campoFinServServicioRefOrigen.val(data.referencia_origen ?? "");
    $campoFinServServicioRefDestino.val(data.referencia_destino ?? "");
    $campoFinServServicioFechaProg.val(data.fecha_programacion ?? "");
    $campoFinServServicioHoraProg.val(data.hora_programacion ?? "");
    $campoFinServServicioPasajeros.val(data.pasajeros ?? "");
    $campoFinServServicioMonto.val(data.monto_servicio ?? "8.00");
    $campoFinServServicioObservacion.val(data.observacion ?? "");

    let horaInicio = data.hora_inicio ?? (data.hora_programacion ?? horaMinActual);
    $campoFinServServicioHoraInicio.val(horaInicio)
    $campoFinServServicioHoraFin.val(data.hora_fin ?? horaMinActual)
  }

  $("#btnFinServCheckFinalizar").click(function () {
    let $checkObj = $(this);
    if ($checkObj.html() == FINALIZAR_NO_CHECKET) {
      $checkObj.html(FINALIZAR_CHECKET);
      $campoFinServCheckFinalizar.val("1");
      $checkObj.removeClass("btn-secondary").addClass("btn-cyan");
    } else {
      $checkObj.html(FINALIZAR_NO_CHECKET);
      $campoFinServCheckFinalizar.val("");
      $checkObj.removeClass("btn-cyan").addClass("btn-secondary");
    }
    // -------- cancelar finalizar
    if ($campoFinServCheckCancelar.val().length > 0) {
      $campoFinServCheckCancelar.val("");
      $("#btnFinServCheckCancelar").removeClass("btn-cyan").addClass("btn-secondary").html(CANCELAR_NO_CHECKET);
    }
  });
  $("#btnFinServCheckCancelar").click(function () {
    let $checkObj = $(this);
    if ($checkObj.html() == CANCELAR_NO_CHECKET) {
      $checkObj.html(CANCELAR_CHECKET);
      $campoFinServCheckCancelar.val("1");
      $checkObj.removeClass("btn-secondary").addClass("btn-cyan");
    } else {
      $checkObj.html(CANCELAR_NO_CHECKET);
      $campoFinServCheckCancelar.val("");
      $checkObj.removeClass("btn-cyan").addClass("btn-secondary");
    }

    // -------- cancelar finalizar
    if ($campoFinServCheckFinalizar.val().length > 0) {
      $campoFinServCheckFinalizar.val("");
      $("#btnFinServCheckFinalizar").removeClass("btn-cyan").addClass("btn-secondary").html(FINALIZAR_NO_CHECKET);
    }
  });

  $("#bntTurnoConductoresView").click(function () {
    $(this).prop("disabled", true);
    $("#bs-turno-conductor-modal-lg").modal("show");
  });
  $("#bntTurnoConductoresCancelar").click(function () {
    $("#bs-turno-conductor-modal-lg").modal("hide");
  });
});
