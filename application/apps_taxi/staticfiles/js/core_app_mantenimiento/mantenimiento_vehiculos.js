var fnTblMantVehiculo = null;
$(document).ready(function () {
  const $modalVehiculo = $("#bs-nuevo-conductor-modal-lg");
  const $btnAgregarVehiculos = $("#btnAgregarVehiculos");
  const $btnMantenerVehiculoGuardar = $("#btnMantenerVehiculoGuardar");
  const $btnMantenerVehiculoCancelar = $("#btnMantenerVehiculoCancelar");

  const $checkVerVehiculosTodosLosEstado = $("#ver_conductores_todos_los_estados");

  const $campoCodigoVehiculo = $("#id_codigo_vehiculo");
  const $campoNombreVehiculo = $("#id_vehiculo_nombre");
  const $campoMarca = $("#id_vehiculo_marca");
  const $campoModelo = $("#id_vehiculo_modelo");
  const $campoMatricula = $("#id_vehiculo_matricula");
  const $campoNumeroVin = $("#id_vehiculo_numero_vin");
  const $campoDescripcion = $("#id_vehiculo_descripcion");
  const $campoObservacion = $("#id_vehiculo_observacion");

  const $tblMantVehiculo = $("#lista-mant-vehiculos");
  const arrayOcultarColumaMantVehiculoDatatable = [1, 9, 10, 11, 12];

  function ocultarColumDatatableMantVehiculo() {
    const filas = $("#lista-mant-vehiculos tbody").find("tr").length;
    if (arrayOcultarColumaMantVehiculoDatatable.length === 0) {
      $("#lista-mant-vehiculos thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-mant-vehiculos tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaMantVehiculoDatatable.map((item) =>
        $("#lista-mant-vehiculos thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaMantVehiculoDatatable.map((item) => $("#lista-mant-vehiculos tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblMantVehiculo = $tblMantVehiculo.DataTable({
    language: {
      "sProcessing": "Procesando...",
      "sLengthMenu": "Mostrar _MENU_ registros",
      "sZeroRecords": "No se encontraron resultados",
      "sEmptyTable": "Ningún dato disponible en esta tabla",
      "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
      "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix": "",
      "sSearch": "Buscar (Nro o Placa):",
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
      url: urlList.vehiculo.listVehiculo,
      method: "get",
      dataType: "json",
      data: function (params) {
        if ($checkVerVehiculosTodosLosEstado.is(":checked")) {
          params["ver_vehiculo_todos_los_estados"] = "si";
        }
        return params;
      },
      dataSrc: function (jsonData) {
        return jsonData.data;
      },
      error: function () {
        swal.fire({
          title: "Alerta Vehiculos - Carga de datos",
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
          $(".modificar-vehiculo").prop("disabled", false);
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
          if (arrayOcultarColumaMantVehiculoDatatable.length > 0) {
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
          return `<label class="label label-default text-dark font-14 pt-1 pb-1 m-0 font-bold"
            title="${data.cod_vehiculo ?? ""}">${data.nom_vehiculo ?? ""}</label>`;
        },
        className: "text-center border-left",
        searchable: false,
        orderable: false,
        width: "100"
      },
      {
        data: function (data) {
          return data.matricula ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.numero_vin ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.marca ?? "";
        },
        className: "text-left",
        searchable: false,
        orderable: false
      },
      {
        data: function (data) {
          return data.modelo ?? "";
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
          return data.estado_vehiculo_text ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.estado_alquilado_text ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.descripcion ?? "-";
        }
      },
      {
        className: "text-center",
        searchable: false,
        orderable: false,
        width: "100",
        data: function (data) {
          return data.observacion ?? "-";
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
          return fnTblMantVehiculo_obtenerOpciones(data);
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableMantVehiculo();
      $(".modificar-vehiculo").prop("disabled", false);
    }
  });

  function fnTblMantVehiculo_obtenerOpciones(data) {
    let btnEstadoCambioEstado = "";
    let htmlAcciones = "";
    const estadoFueraServicio = "02";
    const estadoActivo = "03";
    const estadoEnBaja = "04";
    if ([estadoFueraServicio, estadoActivo].includes(data.estado_vehiculo)) {
      if (data.estado_vehiculo == estadoActivo) {
        btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codvehiculo="${data.cod_vehiculo}"
            class="dropdown-item text-warning cambio-estado-fueraservicio"> Poner fuera servicio </a>
            <div class="dropdown-divider"></div>
            <a href="javascript:void(0)" data-codvehiculo="${data.cod_vehiculo}"
            class="dropdown-item text-primary cambio-estado-darbaja"> Dar de baja</a>`;
      }
      if (data.estado_vehiculo == estadoFueraServicio) {
        btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codvehiculo="${data.cod_vehiculo}"
          class="dropdown-item cambio-estado-activo"> Activo</a>`;
      }
    } else if (data.estado_vehiculo == estadoEnBaja) {
      btnEstadoCambioEstado = `<a href="javascript:void(0)" data-codvehiculo="${data.cod_vehiculo}"
        class="dropdown-item cambio-estado-activo"> Activo</a>`;
    }
    if (btnEstadoCambioEstado != "") {
      htmlAcciones = `<div class="btn-group btn-group-sm">
          <button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown"
           aria-haspopup="true" aria-expanded="false"> Acciones </button>
          <div class="dropdown-menu border border-cyan">${btnEstadoCambioEstado}</div>
        </div>`;
    }
    return `<button type="button" data-codvehiculo="${data.cod_vehiculo}"
      class="btn btn-sm btn-cyan modificar-vehiculo"><i class="fa fa-edit"></i></button>
      ${htmlAcciones}`;
  }

  tblMantVehiculo.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblMantVehiculo.DataTable().page.info();
    tblMantVehiculo.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-mant-vehiculos tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblMantVehiculo.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaMantVehiculoDatatable.map(
        (item) => `<th>${$("#lista-mant-vehiculos thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaMantVehiculoDatatable.map((item) => `<td>${datos[item]}</td>`);
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
  $modalVehiculo.on("show.bs.modal", function () {
    setTimeout(function () {
      // fnTblEscogerVehiculo();
    }, 300);
  });

  $modalVehiculo.on("hide.bs.modal", function () {
    setTimeout(function () {
      fnTblMantVehiculo();
    }, 300);
  });
  // Modal <------
  $("#lista-mant-vehiculos tbody").on("click", ".modificar-vehiculo", function () {
    const $auxBtn = $(this);
    let codigoVehiculo = $auxBtn.data("codvehiculo") ?? "";
    const auxUrl = urlList.vehiculo.mantenerVehiculos.replace("/0000/", `/${codigoVehiculo}/`);
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
        $campoCodigoVehiculo.val(data.cod_vehiculo ?? "");
        $campoNombreVehiculo.val(data.nom_vehiculo ?? "");
        $campoMarca.val(data.marca ?? "");
        $campoModelo.val(data.modelo ?? "");
        $campoMatricula.val(data.matricula ?? "");
        $campoNumeroVin.val(data.numero_vin ?? "");
        $campoDescripcion.val(data.descripcion ?? "");
        $campoObservacion.val(data.observacion ?? "");

        $modalVehiculo.modal("show");
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

  $btnAgregarVehiculos.click(function () {
    $campoCodigoVehiculo.val("");
    $campoNombreVehiculo.val("");
    $campoMarca.val("");
    $campoModelo.val("");
    $campoDescripcion.val("");
    $campoObservacion.val("");
    $campoMatricula.val("");
    $campoNumeroVin.val("");
    $modalVehiculo.modal("show");
  });

  $btnMantenerVehiculoGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const _data = $("#id_frm_mantener_conductor :input").serializeArray();
    const codigoVehiculo = $campoCodigoVehiculo.val();
    const campoNombreVehiculo = $campoNombreVehiculo.val() ?? "";
    let auxUrl = "";
    let auxType = "PATCH";
    if (codigoVehiculo == "") {
      auxUrl = urlList.vehiculo.crearVehiculos;
      auxType = "POST";
      _data.push({name: "action", value: "nuevo"});
    } else {
      auxUrl = urlList.vehiculo.mantenerVehiculos.replace("/0000/", `/${codigoVehiculo}/`);
      _data.push({name: "action", value: "modificar"});
    }
    if (campoNombreVehiculo == "") {
      swal.fire({
        title: "Alerta",
        text: "Número de vehículo",
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
        $modalVehiculo.modal("hide");
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
  $("#lista-mant-vehiculos tbody").on("click", ".cambio-estado-activo", function () {
    const $auxBtnExce = $(this);
    swal.fire({
      title: "Alerta Vehiculo - Modificar estado",
      html: `Se cambiará de estado al conductor a <b>ACTIVO</b>. <br> ¿Desea cambiar de estado?`,
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
        fnActualizarEstadoVehiculo($auxBtnExce, "disponible");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });
  });

  $("#lista-mant-vehiculos tbody").on("click", ".cambio-estado-fueraservicio", function () {
    const $auxBtnExce = $(this);

    swal.fire({
      title: "Alerta Vehiculo - Modificar estado",
      html: `Se cambiará de estado al conductor a <b>Fuera de Servicio</b>. <br> ¿Desea cambiar de estado?`,
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
        fnActualizarEstadoVehiculo($auxBtnExce, "ausente");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  $("#lista-mant-vehiculos tbody").on("click", ".cambio-estado-darbaja", function () {
    const $auxBtnExce = $(this);

    swal.fire({
      title: "Alerta Vehiculo - Modificar estado",
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
        fnActualizarEstadoVehiculo($auxBtnExce, "darbaja");
        return true;
      }
      $auxBtnExce.prop("disabled", false);
    });

  });

  function fnActualizarEstadoVehiculo($auxBtnExce, estado = "") {
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoVehiculo = $auxBtnExce.data("codvehiculo");
    $.ajax({
      url: urlList.vehiculo.mantenerVehiculos.replace("/0000/", `/${codigoVehiculo}/`),
      type: "PATCH",
      dataType: "json",
      data: [{name: "action", value: estado}, {name: "codigo_vehiculo", value: codigoVehiculo}],
      headers: {"X-CSRFToken": csrfToken},
      beforeSend: function () {
        $auxBtnExce.prop("disabled", true);
      },
      success: function (resp) {
        $auxBtnExce.prop("disabled", false);
        fnTblMantVehiculo();
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

  $btnMantenerVehiculoCancelar.click(function () {
    $modalVehiculo.modal("hide");
  });

  $checkVerVehiculosTodosLosEstado.click(function () {
    fnTblMantVehiculo();
  });

  fnTblMantVehiculo = function () {
    try {
      tblMantVehiculo.search("");
      tblMantVehiculo.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblMantVehiculo();

});
