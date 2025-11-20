$(document).ready(function () {
  const $btnIniciarTurnoOperador = $(".btnIniciarTurnoOperador");
  const $btnCerrarTurnoOperador = $("#btnCerrarTurnoOperador");
  const $btnCerrarTurnoPreView = $("#btnCerrarTurnoPreView");

  function fnIniciarTurnoOperador($auxBtnExce) {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoTurno = $auxBtnExce.data("codigoturno") ?? "";
    let _url = urlList.sesion.iniciarTurnoOperador.replace("/0000/", `/${codigoTurno}/`);
    const _data = {"codigo_turno": codigoTurno};
    $.ajax({
      url: _url,
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        let respCodigoTurno = resp.data.id ?? "";
        if (respCodigoTurno.toString() === codigoTurno.toString()) {
          swal.fire({
            title: "Inicio de Turno Operador",
            text: "Se inició correctamente",
            type: "success",
            showConfirmButton: true, confirmButtonText: "Cerrar",
          }).then(function (isConfirmed) {
            if (!isConfirmed.value) {
              location.href = urlAccessList.dashboardPage;
            }
          });
          return true;
        }

        swal.fire({
          title: "Inicio de Turno Operador",
          text: "Datos no validos, volver a intentar",
          type: "error",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        }).then(function (isConfirmed) {
          if (isConfirmed.value) {
            $campoUserName.val("");
          }
          $campoUserPasswor.val("");
        });
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se inició turno";
        }
        swal.fire({
          title: "Iniciar Turno",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }

  function fnCerrarTurnoOperador($auxBtnExce) {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoTurno = $auxBtnExce.data("codigoturno") ?? "";
    let _url = urlList.sesion.cerrarTurnoOperador.replace("/0000/", `/${codigoTurno}/`);
    const _data = {"codigo_turno": codigoTurno};
    $.ajax({
      url: _url,
      type: "PATCH",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        let respCodigoTurno = resp.data.id ?? "";
        if (respCodigoTurno.toString() === codigoTurno.toString()) {
          swal.fire({
            title: "Se Cerró el Turno Operador",
            text: "se cerró correctamente",
            type: "success",
            showConfirmButton: true, confirmButtonText: "Cerrar",
          }).then(function (isConfirmed) {
            if (isConfirmed.value) {
              location.href = urlAccessList.dashboardPage;
            }
          });
          return true;
        }

        swal.fire({
          title: "Cerrar Turno Operador",
          text: "Datos no validos, volver a intentar",
          type: "error",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        }).then(function (isConfirmed) {
          if (isConfirmed.value) {
            $campoUserName.val("");
            $campoUserPasswor.val("");
          }
        });
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se cerró el turno";
        }
        swal.fire({
          title: "Cerrar Turno",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }


  $btnIniciarTurnoOperador.click(function () {
    const $auxBtnExce = $(this);
    let horario = $auxBtnExce.data("horario") ?? "";
    let fecha = $auxBtnExce.data("fecha") ?? "";
    swal.fire({
      title: "Alerta iniciar Turnos del operador",
      html: `Se activará fecha <b>${fecha}</b> turno <b>${horario}</b>. <br> ¿Desea activar turno?`,
      type: "warning",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonText: "Confirmar",
      cancelButtonText: "Cancelar"
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnIniciarTurnoOperador($auxBtnExce);
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  $btnCerrarTurnoOperador.click(function () {
    const $auxBtnExce = $(this);
    let horario = $auxBtnExce.data("horario") ?? "";
    let fecha = $auxBtnExce.data("fecha") ?? "";
    swal.fire({
      title: "Alerta cerrar Turnos del operador",
      html: `Se cerrará turno del operador fecha <b>${fecha}</b> turno <b>${horario}</b>. <br> ¿Desea cerrar turno?`,
      type: "warning",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonText: "Confirmar",
      cancelButtonText: "Cancelar"
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnCerrarTurnoOperador($auxBtnExce);
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  $btnCerrarTurnoPreView.click(function () {
    const $auxBtnExce = $(this);
    $.ajax({
      url: urlList.turno.resumenCerrarTurno,
      type: "GET",
      dataType: "json",
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        const turno_operador = ((resp ?? {}).data ?? {}).turno_operador ?? {};
        $auxBtnExce.prop("disabled", false);
        $("#bs-cerrar-turno-modal-lg").modal("show");
        setTimeout(function () {
          $("#id-llamadas-recibidas").html(turno_operador.llamadas_atendidos) ?? "-";
          $("#id-llamadas-atendidas").html(turno_operador.servicios_asignadas) ?? "-";
          $("#id-llamadas-creadas").html(turno_operador.servicios_registradas) ?? "-";
          $("#id-llamadas-noatendidas").html("-");
        }, 300);
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.error.message;
        } catch (e) {
          mensaje = "No se llego logear";
        }
        swal.fire({
          title: "Login",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  });

  $("#btnCerrarSesionTurno").click(function () {
    $("#btnCerrarTurnoOperador").click();
  });
  $("#btnCancelarSesionTurno").click(function () {
    $("#bs-cerrar-turno-modal-lg").modal("hide");
  });

});
