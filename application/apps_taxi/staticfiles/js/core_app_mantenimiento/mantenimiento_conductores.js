var fnTblMantConductor = null;
$(document).ready(function () {
  const $modalConductor = $("#bs-nuevo-conductor-modal-lg");
  const $btnAgregarConductores = $("#btnAgregarConductores");
  const $btnMantenerConductorGuardar = $("#btnMantenerConductorGuardar");
  const $btnMantenerConductorCancelar = $("#btnMantenerConductorCancelar");

  const $checkVerConductoresTodosLosEstado = $("#ver_conductores_todos_los_estados");

  const $campoCodigoConductor = $("#id_codigo_conductor");
  const $campoNombreConductor = $("#id_conductor_nombres");
  const $campoApellidoPatConductor = $("#id_conductor_apellido_paterno");
  const $campoApellidoMatConductor = $("#id_conductor_apellido_materno");
  const $campoTelefonoConductor = $("#id_conductor_telefono");
  const $campoDireccionConductor = $("#id_conductor_direccion");
  const $campoConductorLicencia = $("#id_conductor_licencia");
  const $campoConductorClase = $("#id_conductor_clase");
  const $campoConductorFechaVencimiento = $("#id_conductor_fecha_vencimiento");
  const $campoConductorEstadoEeuu = $("#id_conductor_estado_eeuu");

  const $tblMantConductor = $("#lista-mant-conductores");
  const arrayOcultarColumaMantConductorDatatable = [0, 1, 2, 8, 9];

  function ocultarColumDatatableMantConductor() {
    const filas = $("#lista-mant-conductores tbody").find("tr").length;
    if (arrayOcultarColumaMantConductorDatatable.length === 0) {
      $("#lista-mant-conductores thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-mant-conductores tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaMantConductorDatatable.map((item) =>
        $("#lista-mant-conductores thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaMantConductorDatatable.map((item) => $("#lista-mant-conductores tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblMantConductor = $tblMantConductor.DataTable({
    language: {
      "sProcessing": "Procesando...",
      "sLengthMenu": "Mostrar _MENU_ registros",
      "sZeroRecords": "No se encontraron resultados",
      "sEmptyTable": "Ningún dato disponible en esta tabla",
      "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
      "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix": "",
      "sSearch": "Buscar (Licencia, Nombres o Apellido Paterno):",
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
      url: urlList.conductor.listaConductores,
      method: "get",
      dataType: "json",
      data: function (params) {
        if ($checkVerConductoresTodosLosEstado.is(":checked")) {
          params["ver_conductor_todos_los_estados"] = "si";
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        swal.fire({
          title: "Alerta Conductores - Carga de datos",
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
          $(".modificar-conductor").prop("disabled", false);
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
          if (arrayOcultarColumaMantConductorDatatable.length > 0) {
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
          return `<span class="text-black-50">${data.cod_conductor ?? ""}</span>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "100"
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.licencia ?? "-";
        }
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
        width: "100",
        data: function (data) {
          return data.telefono ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.direccion ?? "-";
        }
      },
      // {
      //   className: "text-center",
      //   searchable: false,
      //   orderable: false,
      //   width: "100",
      //   data: function (data) {
      //     return data.clase ?? "-";
      //   }
      // },
      // {
      //   className: "text-center",
      //   searchable: false,
      //   orderable: false,
      //   width: "100",
      //   data: function (data) {
      //     return data.fecha_vencimiento ?? "-";
      //   }
      // },
      // {
      //   className: "text-center",
      //   searchable: false,
      //   orderable: false,
      //   width: "100",
      //   data: function (data) {
      //     return data.estado_eeuu ?? "-";
      //   }
      // },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "180",
        data: function (data) {
          let btnEstadoCambioEstado = "";
          let htmlAcciones = "";
          const estadoAusente = "02";
          const estadoDisponible = "04";
          const estadoEnBaja = "05";
          if ([estadoAusente, estadoDisponible].includes(data.estado)) {
            if (data.estado == estadoDisponible) {
              btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codconductor="${data.cod_conductor}"
                class="dropdown-item text-warning cambio-estado-ausente"> Poner ausente </a>
                <div class="dropdown-divider"></div>
                <a href="javascript:void(0)" data-codconductor="${data.cod_conductor}"
                class="dropdown-item text-primary cambio-estado-darbaja"> Dar de baja</a>
              `;
            }
            if (data.estado == estadoAusente) {
              btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codconductor="${data.cod_conductor}"
                class="dropdown-item cambio-estado-disponible"> Disponible</a>`;
            }
          } else if (data.estado == estadoEnBaja) {
            btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codconductor="${data.cod_conductor}"
                class="dropdown-item cambio-estado-disponible"> Disponible</a>`;
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
          return `<button type="button" data-codconductor="${data.cod_conductor}"
                class="btn btn-sm btn-cyan modificar-conductor"><i
                class="fa fa-edit"></i></button>
                ${htmlAcciones}`;
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableMantConductor();
      $(".modificar-conductor").prop("disabled", false);
    }
  });

  tblMantConductor.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblMantConductor.DataTable().page.info();
    tblMantConductor.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-mant-conductores tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblMantConductor.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaMantConductorDatatable.map(
        (item) => `<th>${$("#lista-mant-conductores thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaMantConductorDatatable.map((item) => `<td>${datos[item]}</td>`);
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
  $modalConductor.on("show.bs.modal", function () {
    setTimeout(function () {
      // fnTblEscogerConductor();
    }, 300);
  });

  $modalConductor.on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblMantConductor();
    }, 300);
  });
  // Modal <------
  $("#lista-mant-conductores tbody").on("click", ".modificar-conductor", function () {
    const $auxBtn = $(this);
    let codigoConductor = $auxBtn.data("codconductor") ?? "";
    const auxUrl = urlList.conductor.mantenerConductores.replace("/0000/", `/${codigoConductor}/`);
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
        $campoCodigoConductor.val(data.cod_conductor ?? "");
        $campoNombreConductor.val(data.nombre ?? "");
        $campoApellidoPatConductor.val(apePat.replace("-", ""));
        $campoApellidoMatConductor.val(apeMat.replace("-", ""));
        $campoTelefonoConductor.val(data.telefono ?? "");
        $campoDireccionConductor.val(data.direccion ?? "");
        $campoConductorLicencia.val(data.licencia ?? "");
        $campoConductorClase.val(data.clase ?? "");
        $campoConductorFechaVencimiento.val(data.fecha_vencimiento ?? "");
        $campoConductorEstadoEeuu.val(data.estado_eeuu ?? "");
        $modalConductor.modal("show");
        $auxBtn.prop("disabled", false);
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

  $btnAgregarConductores.click(function () {
    $campoCodigoConductor.val("");
    $campoNombreConductor.val("");
    $campoApellidoPatConductor.val("");
    $campoApellidoMatConductor.val("");
    $campoTelefonoConductor.val("");
    $campoDireccionConductor.val("");
    $campoConductorLicencia.val("");
    $campoConductorClase.val("");
    $campoConductorFechaVencimiento.val("");
    $campoConductorEstadoEeuu.val("");
    $modalConductor.modal("show");
  });

  $btnMantenerConductorGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#id_frm_mantener_conductor :input").serializeArray();
    const codigoConductor = $campoCodigoConductor.val();
    const campoNombreConductor = $campoNombreConductor.val() ?? "";
    const campoApellidoPatConductor = $campoApellidoPatConductor.val() ?? "";
    let auxUrl = "";
    let auxType = "PATCH";
    if (codigoConductor == "") {
      auxUrl = urlList.conductor.crearConductores;
      auxType = "POST";
      _data.push({name: "action", value: "nuevo"});
    } else {
      auxUrl = urlList.conductor.mantenerConductores.replace("/0000/", `/${codigoConductor}/`);
      _data.push({name: "action", value: "modificar"});
    }
    if (campoNombreConductor == "") {
      swal.fire({
        title: "Alerta",
        text: "Nombre de conductor",
        type: "warning",
        showConfirmButton: true, confirmButtonText: "Cerrar",
      });
      return false;
    }
    if (campoApellidoPatConductor == "") {
      swal.fire({
        title: "Alerta",
        text: "Apellidopaterno del conductor",
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
        $modalConductor.modal("hide");
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
  $("#lista-mant-conductores tbody").on("click", ".cambio-estado-disponible", function () {
    const $auxBtnExce = $(this);
    swal.fire({
      title: "Alerta Conductor - Modificar estado",
      html: `Se cambiará de estado al conductor a <b>DISPONIBLE</b>. <br> ¿Desea cambiar de estado?`,
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
        fnActualizarEstadoConductor($auxBtnExce, "disponible");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });
  });

  $("#lista-mant-conductores tbody").on("click", ".cambio-estado-ausente", function () {
    const $auxBtnExce = $(this);

    swal.fire({
      title: "Alerta Conductor - Modificar estado",
      html: `Se cambiará de estado al conductor a <b>AUSENTE</b>. <br> ¿Desea cambiar de estado?`,
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
        fnActualizarEstadoConductor($auxBtnExce, "ausente");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  $("#lista-mant-conductores tbody").on("click", ".cambio-estado-darbaja", function () {
    const $auxBtnExce = $(this);

    swal.fire({
      title: "Alerta Conductor - Modificar estado",
      html: `Se dará de <b>BAJA</b> al conductor. <br> ¿Desea cambiar ejecutar la acción?`,
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
        fnActualizarEstadoConductor($auxBtnExce, "darbaja");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  function fnActualizarEstadoConductor($auxBtnExce, estado = "") {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoConductor = $auxBtnExce.data("codconductor");
    $.ajax({
      url: urlList.conductor.mantenerConductores.replace("/0000/", `/${codigoConductor}/`),
      type: "PATCH",
      dataType: "json",
      data: [{name: "action", value: estado}, {name: "codigo_conductor", value: codigoConductor}],
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        fnTblMantConductor();
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

  $btnMantenerConductorCancelar.click(function () {
    $modalConductor.modal("hide");
  });

  $checkVerConductoresTodosLosEstado.click(function () {
    fnTblMantConductor();
  });

  fnTblMantConductor = function () {
    try {
      tblMantConductor.search("");
      tblMantConductor.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblMantConductor();

});
