const $campoAtenderLlamdaServicioTurno = $("#id_servicio_turno");
$(document).ready(function () {
  const $frmLogin = $("#frmLoginUserFront");
  const $campoUserName = $("#id_user_name");
  const $campoUserPasswor = $("#id_user_password");
  const $btnAccederLogin = $("#btnAccederLogin");

  $btnAccederLogin.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#frmLoginUserFront :input").serializeArray();
    $.ajax({
      url: urlAccessList.access.logIn,
      type: "POST",
      dataType: "json",
      data: _data,
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        if (resp.login) {
          swal.fire({
            title: "Login",
            text: "Acceso correcto",
            type: "success",
            showConfirmButton: true, confirmButtonText: "Cerrar",
          }).then(function (isConfirmed) {
            location.href = urlAccessList.dashboardPage;
          });
          return true;
        }

        swal.fire({
          title: "Login",
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

});
