$(document).ready(function () {
  function fnAccessLogOut(auxObjBnt) {
    const $auxBtnExce = $(auxObjBnt);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";

    $.ajax({
      url: urlAccessList.access.logOut,
      type: "GET",
      dataType: "json",
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        location.href = urlAccessList.dashboardLogin;
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.data_ws.error.message;
        } catch (e) {
          mensaje = "No se llego cerrar sesión";
        }
        swal.fire({
          title: "Login",
          text: mensaje,
          type: "warning",
          showConfirmButton: true, confirmButtonText: "Cerrar",
        });
      }
    });
  }

  $(".btnAccessLogOut").click(function () {
    const $btnAux = $(this);
    swal.fire({
      title: "Alerta",
      html: `¿Desea salir del Sistema?`,
      type: "warning",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> Confirmar",
      cancelButtonText: "<i class='fa fa-times'></i> Cancelar"
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnAccessLogOut($btnAux);
        return true;
      }
    });
  });

});
