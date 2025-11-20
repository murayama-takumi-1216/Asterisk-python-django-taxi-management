var fnTblMantOperador = null;
$(document).ready(function () {
  const $btnAgregarOperador = $("#btnAgregarOperador");

  const $checkVerOperadoresTodosLosEstado = $("#ver_operadores_todos_los_estados");

  const $modalOperador = $("#bs-nuevo-operador-modal-lg");
  const $btnMantenerOperadorGuardar = $("#btnMantenerOperadorGuardar");
  const $btnMantenerOperadorCancelar = $("#btnMantenerOperadorCancelar");
  // ----------
  const $campoCodigoOperador = $("#id_codigo_operador");
  const $campoNombreOperador = $("#id_operador_nombres");
  const $campoApellidoPatOperador = $("#id_operador_apellido_paterno");
  const $campoApellidoMatOperador = $("#id_operador_apellido_materno");
  const $campoExtension = $("#id_operador_extension");
  const $campoAlias = $("#id_operador_alias");

  const $modalCrearUsuario = $("#bs-operador-crearusuario-modal-lg");
  const $btnCrearOperadorGuardar = $("#btnCrearUsuarioOperadorGuardar");
  const $btnCrearOperadorCancelar = $("#btnCrearUsuarioOperadorCancelar");
  // -------
  const $campoCodigoOperadorCrear = $("#id_crearusuario_codigo_operador");
  const $campoNombreUsuarioCrear = $("#id_crearusuario_operador_usuario");
  const $campoClaveCrear = $("#id_crearusuario_operador_clave");
  const $campoRepetirClave = $("#id_crearusuario_operador_repetirclave");

  const $modalCambiarClave = $("#bs-operador-cambiarclave-modal-lg");
  const $btnCambiarClaveOperadorGuardar = $("#btnCambiarClaveOperadorGuardar");
  const $btnCambiarClaveOperadorCancelar = $("#btnCambiarClaveOperadorCancelar");
  // -------
  const $campoCodigoOperadorModificar = $("#id_cambiarclave_codigo_operador");
  const $campoNombreUsuarioModificar = $("#id_cambiarclave_operador_usuario");
  const $campoClaveModificar = $("#id_cambiarclave_operador_clave");
  const $campoRepetirClaveModificar = $("#id_cambiarclave_operador_repetirclave");

  const $tblMantOperador = $("#lista-mant-operadores");
  const arrayOcultarColumaMantOperadorDatatable = [1, 2, 8, 9];

  function ocultarColumDatatableMantOperador() {
    const filas = $("#lista-mant-operadores tbody").find("tr").length;
    if (arrayOcultarColumaMantOperadorDatatable.length === 0) {
      $("#lista-mant-operadores thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-mant-operadores tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaMantOperadorDatatable.map((item) =>
        $("#lista-mant-operadores thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaMantOperadorDatatable.map((item) => $("#lista-mant-operadores tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblMantOperador = $tblMantOperador.DataTable({
    language: {
      "sProcessing": "Procesando...",
      "sLengthMenu": "Mostrar _MENU_ registros",
      "sZeroRecords": "No se encontraron resultados",
      "sEmptyTable": "Ningún dato disponible en esta tabla",
      "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
      "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix": "",
      "sSearch": "Buscar (Nombres o Apellido Paterno):",
      "sUrl": "",
      "sInfoThousands": ",",
      "sLoadingRecords": "Cargando...",
      "oPaginate": {
        "sFirst": "Primero",
        "sLast": "Último",
        "sNext": "Siguiente",
        "sPrevious": "Anterior"
      },
      "oAria": {
        "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
      }
    },
    serverSide: true,
    destroy: true,
    deferRender: false,
    deferLoading: 0,
    searchDelay: 350,
    processing: true,
    searching: true,//false//true:boton
    displayLength: 10,
    paging: true,
    lengthMenu: [10, 20, 30, 40, 60],
    pagingDelay: 1000,
    responsive: true,
    ajax: {
      cache: false,
      url: urlList.operador.listOperadores,
      method: "get",
      dataType: "json",
      data: function (params) {
        if ($checkVerOperadoresTodosLosEstado.is(":checked")) {
          params["ver_operador_todos_los_estados"] = "si";
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        swal.fire({
          title: "Alerta Operadores - Carga de datos",
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
          $(".modificar-operador").prop("disabled", false);
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
          if (arrayOcultarColumaMantOperadorDatatable.length > 0) {
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
          return `<span class="text-black-50">${data.codigo ?? ""}</span>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "100"
      },
      {
        data: function (data) {
          return data.nombre ?? "";
        },
        className: "text-left border-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.apellido_paterno ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.apellido_materno ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "150",
        data: function (data) {
          let userName = (data.user_name ?? "").trim();
          let btnData = ` data-codoperador="${data.codigo}" data-usuario="${userName}"
            data-nombre="${data.nombre ?? ""}" data-apellidopat="${data.apellido_paterno ?? ""}"`;
          let btnCrearUsuario = "";
          if (userName.length < 1) {
            btnCrearUsuario = `<button type="button" ${btnData}
                class="btn btn-sm btn-cyan agregar-usuario"><i
                class="ti-plus"></i></button>`;
          }
          let btnCambiarClave = "";
          if (userName.length > 0) {
            btnCambiarClave = `<button type="button"  ${btnData}
                class="btn btn-sm btn-cyan cambiar-clave"><i
                class="ti-key"></i></button>`;
          }
          return `${btnCrearUsuario} ${btnCambiarClave} ${userName}`;
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.estado_text ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.modified ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.modified_by ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "180",
        data: function (data) {
          let btnEstadoCambioEstado = "";
          let htmlAcciones = "";
          const estadoDisponible = true;
          const estadoEnBaja = false;
          if (data.estado === estadoDisponible) {
            btnEstadoCambioEstado = `
              <a href="javascript:void(0)" data-codoperador="${data.codigo}"
              class="dropdown-item text-primary cambio-estado-darbaja"> Inactivar</a>`;
          } else if (data.estado === estadoEnBaja) {
            btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codoperador="${data.codigo}"
              class="dropdown-item cambio-estado-activo"> Activar</a>`;
          }
          if (btnEstadoCambioEstado != "") {
            htmlAcciones = `<div class="btn-group btn-group-sm">
                <button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Acciones
                </button>
                <div class="dropdown-menu border border-cyan">
                  ${btnEstadoCambioEstado}
                </div>
              </div>`;
          }
          return `<button type="button" data-codoperador="${data.codigo}"
                class="btn btn-sm btn-cyan modificar-operador"><i
                class="fa fa-edit"></i></button>
                ${htmlAcciones}`;
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableMantOperador();
      $(".modificar-operador").prop("disabled", false);
    }
  });

  tblMantOperador.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblMantOperador.DataTable().page.info();
    tblMantOperador.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-mant-operadores tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblMantOperador.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaMantOperadorDatatable.map(
        (item) => `<th>${$("#lista-mant-operadores thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaMantOperadorDatatable.map((item) => `<td>${datos[item]}</td>`);
      var htmlInfo = `
        <table class="table table-responsive table-bordered">
        <thead><tr class="table-light">${dataCabecera.join("")}</tr></thead>
        <tbody><tr>${dataDesc.join("")}</tr></tbody>
        </table>`;
      row.child(htmlInfo).show();
      tr.addClass("shown");
    }
  });

  // Modal ------>
  $modalOperador.on("show.bs.modal", function () {
    // setTimeout(function () {
    //   fnTblMantOperador();
    // }, 300);
  });

  $modalOperador.on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblMantOperador();
    }, 300);
  });

  $modalCrearUsuario.on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblMantOperador();
    }, 300);
  });
  // Modal <------
  $("#lista-mant-operadores tbody").on("click", ".modificar-operador", function () {
    const $auxBtn = $(this);
    let codigoOperador = $auxBtn.data("codoperador") ?? "";
    const auxUrl = urlList.operador.mantenerOperador.replace("/0000/", `/${codigoOperador}/`);
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
        let permiteModificarDataInicial = resp.modificar ?? true;
        let data = resp.data ?? {};
        let apePat = data.apellido_paterno ?? "";
        let apeMat = data.apellido_materno ?? "";
        $campoCodigoOperador.val(data.codigo ?? "");
        $campoNombreOperador.val(data.nombre ?? "");
        $campoApellidoPatOperador.val(apePat.replace("-", ""));
        $campoApellidoMatOperador.val(apeMat.replace("-", ""));
        $campoAlias.val(data.alias ?? "");
        $campoExtension.val(data.extension ?? "");
        $modalOperador.modal("show");
        $auxBtn.prop("disabled", false);
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.detail.message;
        } catch (e) {
          mensaje = "No se llego obtener";
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

  $btnAgregarOperador.click(function () {
    $campoCodigoOperador.val("");
    $campoNombreOperador.val("");
    $campoApellidoPatOperador.val("");
    $campoApellidoMatOperador.val("");
    $campoExtension.val("");
    $campoAlias.val("");
    $modalOperador.modal("show");
  });

  $("#lista-mant-operadores tbody").on("click", ".agregar-usuario", function () {
    const $btnAux = $(this);
    $campoCodigoOperadorCrear.val($btnAux.data("codoperador") ?? "");
    $("#id_crearusuario_operador_nombres").val($btnAux.data("nombre") ?? "");
    $("#id_crearusuario_operador_apellidos").val($btnAux.data("apellidopat") ?? "");
    $campoNombreUsuarioCrear.val("");
    $campoClaveCrear.val("");
    $campoRepetirClave.val("");
    $modalCrearUsuario.modal("show");
  });

  $("#lista-mant-operadores tbody").on("click", ".cambiar-clave", function () {
    const $btnAux = $(this);
    $campoCodigoOperadorModificar.val($btnAux.data("codoperador") ?? "");
    $("#id_cambiarclave_operador_nombres").val($btnAux.data("nombre") ?? "");
    $("#id_cambiarclave_operador_apellidos").val($btnAux.data("apellidopat") ?? "");
    $campoNombreUsuarioModificar.val($btnAux.data("usuario") ?? "");
    $campoClaveModificar.val("");
    $campoRepetirClaveModificar.val("");
    $modalCambiarClave.modal("show");
  });

  $btnMantenerOperadorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#id_frm_mantener_operador :input").serializeArray();
    const codigoOperador = $campoCodigoOperador.val();
    const campoNombreOperador = $campoNombreOperador.val() ?? "";
    const campoApellidoPatOperador = $campoApellidoPatOperador.val() ?? "";
    let auxUrl = "";
    let auxType = "PATCH";
    if (codigoOperador == "") {
      auxUrl = urlList.operador.crearOperador;
      auxType = "POST";
      _data.push({name: "action", value: "nuevo"});
    } else {
      auxUrl = urlList.operador.mantenerOperador.replace("/0000/", `/${codigoOperador}/`);
      _data.push({name: "action", value: "modificar"});
    }
    if (campoNombreOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "Nombre de operador",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    if (campoApellidoPatOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "Apellido Paterno del operador",
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
        $modalOperador.modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.detail.message;
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

  $btnCrearOperadorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#id_frm_mantener_operador_crearusuario :input").serializeArray();
    const codigoOperador = $campoCodigoOperadorCrear.val();
    const nombreUsOperador = $campoNombreUsuarioCrear.val();
    const claveUsOperador = $campoClaveCrear.val();
    const claveRepUsOperador = $campoRepetirClave.val();
    const auxType = "POST";
    const auxUrl = urlList.operador.crearUsuarioOperador;
    _data.push({name: "action", value: "nuevo"});
    if (nombreUsOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "Nombre de usuario del operador",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    if (codigoOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "No existe identificador del operador",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    if (claveUsOperador == "" || (claveUsOperador != claveRepUsOperador)) {
      swal.fire({
        title: "Alerta",
        text: "La clave deber ser igual",
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
        $modalCrearUsuario.modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.detail.message;
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

  $btnCambiarClaveOperadorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#id_frm_mantener_operador_cambiarclave :input").serializeArray();
    const codigoOperador = $campoCodigoOperadorModificar.val();
    const nombreUsOperador = $campoNombreUsuarioModificar.val();
    const claveUsOperador = $campoClaveModificar.val();
    const claveRepUsOperador = $campoRepetirClaveModificar.val();
    const auxType = "PATCH";
    const auxUrl = urlList.operador.mantenerUsuarioOperador.replace("/0000/", `/${codigoOperador}/`);
    _data.push({name: "action", value: "modificar"});
    if (codigoOperador == "") {
      swal.fire({
        title: "Alerta",
        text: "No existe identificador del operador",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    if (claveUsOperador == "" || (claveUsOperador != claveRepUsOperador)) {
      swal.fire({
        title: "Alerta",
        text: "La clave deber ser igual",
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
        $modalCambiarClave.modal("hide");
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.detail.message;
        } catch (e) {
          mensaje = "No se llego actualizar";
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

  $("#lista-mant-operadores tbody").on("click", ".cambio-estado-activo", function () {
    const $auxBtnExce = $(this);
    swal.fire({
      title: "Alerta Operador - Modificar estado",
      html: `Se cambiará de estado al operador a <b>DISPONIBLE</b>. <br> ¿Desea cambiar de estado?`,
      type: "info",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: `Confirmar`,
      cancelButtonText: `Cancelar`
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnActualizarEstadoOperador($auxBtnExce, "activar");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });
  });

  $("#lista-mant-operadores tbody").on("click", ".cambio-estado-darbaja", function () {
    const $auxBtnExce = $(this);

    swal.fire({
      title: "Alerta Operador - Modificar estado",
      html: `Se dará de <b>BAJA</b> al operador. <br> ¿Desea cambiar ejecutar la acción?`,
      type: "info",
      allowOutsideClick: false,
      allowEscapeKey: true,
      showConfirmButton: true,
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: `Confirmar`,
      cancelButtonText: `Cancelar`
    }).then(function (isConfirmed) {
      if (isConfirmed.value) {
        fnActualizarEstadoOperador($auxBtnExce, "darbaja");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  function fnActualizarEstadoOperador($auxBtnExce, estado = "") {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoOperador = $auxBtnExce.data("codoperador");
    $.ajax({
      url: urlList.operador.mantenerOperador.replace("/0000/", `/${codigoOperador}/`),
      type: "PATCH",
      dataType: "json",
      data: [{name: "action", value: estado}, {name: "codigo_operador", value: codigoOperador}],
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        fnTblMantOperador();
      },
      error: function (request, status, data) {
        $auxBtnExce.prop("disabled", false);
        let mensaje = "";
        try {
          mensaje = request.responseJSON.detail.message;
        } catch (e) {
          mensaje = "No se llego actualizar";
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

  $btnMantenerOperadorCancelar.click(function () {
    $modalOperador.modal("hide");
  });

  $btnCrearOperadorCancelar.click(function () {
    $modalCrearUsuario.modal("hide");
  });

  $btnCambiarClaveOperadorCancelar.click(function () {
    $modalCambiarClave.modal("hide");
  });

  $checkVerOperadoresTodosLosEstado.click(function () {
    fnTblMantOperador();
  });

  fnTblMantOperador = function () {
    try {
      tblMantOperador.search("");
      tblMantOperador.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblMantOperador();

});
