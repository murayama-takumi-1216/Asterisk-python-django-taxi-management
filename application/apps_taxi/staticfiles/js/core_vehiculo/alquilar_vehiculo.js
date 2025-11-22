var fnTblAlquilerVehiculo = null;
const $campoBsSelectConductorCodigo = $("#id_bs_select_conductor_codigo");
$(document).ready(function () {
  const $campoBsSelectAlquilerCodigo = $("#id_bs_select_alquiler_codigo");
  const $campoBsSelectVehiculoCodigo = $("#id_bs_select_vehiculo_codigo");

  const $idAlquilerCheckOpcFinalizar = $("#idAlquilerCheckOpcFinalizar");
  const $idAlquilerCampoFinalizar = $("#id_alquiler_finalizar");
  const $btnAlquilerFinalizar = $("#btnAlquilerFinalizar");

  const $idAlquilerOpcInicioHoraActual = $("#idAlquilerOpcInicioHoraActual");
  const $btnAlquilerInicioHoraActual = $("#btnAlquilerInicioHoraActual");

  const $btnFrmAlquilerGuardar = $("#btnFrmAlquilerGuardar");
  const $btnFrmAlquilerCancelar = $("#btnFrmAlquilerCancelar");

  const $tblAlquilerVehiculo = $("#lista-alquiler-vehiculo");
  const arrayOcultarColumaAlquilerVehiculoDatatable = [1, 3];

  function ocultarColumDatatableAlquilerVehiculo() {
    const filas = $("#lista-alquiler-vehiculo tbody").find("tr").length;
    if (arrayOcultarColumaAlquilerVehiculoDatatable.length === 0) {
      $("#lista-alquiler-vehiculo thead tr").find("th").eq(0).hide();
      for (x = 0; x < filas; x++) {
        $("#lista-alquiler-vehiculo tbody tr").eq(x).find("td").eq(0).hide();
      }
    } else {
      arrayOcultarColumaAlquilerVehiculoDatatable.map((item) =>
        $("#lista-alquiler-vehiculo thead tr").find("th").eq(item).hide()
      );
      for (x = 0; x < filas; x++) {
        arrayOcultarColumaAlquilerVehiculoDatatable.map((item) => $("#lista-alquiler-vehiculo tbody tr").eq(x).find("td").eq(item).hide()
        );
      }
    }
  }

  const tblAlquilerVehiculo = $tblAlquilerVehiculo.DataTable({
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
    lengthMenu: [10, 20, 30, 40, 60, 80, 120],
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
        width: "208",
        data: function (data) {
          return data.estado_vehiculo_text;
        }
      },
      {
        className: "text-left",
        searchable: false,
        orderable: false,
        width: "208",
        data: function (data) {
          return data.estado_alquilado_text;
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
          let tieneRadio = "";
          if (Object.keys(alquileres).length > 0) {
            for (i in alquileres) {
              alquiler = alquileres[i] ?? {};
              conductor = alquiler.conductor ?? {};
              nombreConductor = `${conductor.nombre ?? ""} ${conductor.apellido_paterno ?? ""}`;
              alquilerFecha = `[${alquiler.fecha_inicio ?? ""} - ${alquiler.fecha_prog_fin ?? "*"}]`;
              tieneRadio = (alquiler.entrega_radio == true) ? "Con" : "Sin";
              htmlAlquileres += `<button type="button"
                data-codigoalquilado="${alquiler.codigo ?? ""}" class="btn btn-sm btn-cyan editar-alquiler"><i
                class="fa fa-edit"></i></button> ${nombreConductor} <span class="text-black-50">${alquilerFecha}</span>
                <span> ${tieneRadio} radio</span>`;
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
        width: "120",
        data: function (data) {
          let alquileres = data.alquiler_data ?? {};
          let contarAlquileres = Object.keys(alquileres).length;
          if (contarAlquileres > 0) {
            // Get the first rental id to delete
            let alquilerId = "";
            for (let key in alquileres) {
              alquilerId = alquileres[key].id ?? "";
              break;
            }
            return `<button type="button" data-codigoalquilado="${alquilerId}"
              data-codigovehiculo="${data.cod_vehiculo ?? ""}"
              class="btn btn-sm btn-danger eliminar-alquiler"><i
              class="fa fa-ban"></i></button>`;
          }
          let atributosData = `data-codigovehiculo="${data.cod_vehiculo ?? ""}"
              data-nombrevehiculo="${data.nom_vehiculo ?? ""}" data-codigoalquilado=""`;
          return `<button type="button" ${atributosData} class="btn btn-sm btn-cyan agregar-alquiler"><i
              class="fa fa-plus"></i></button>`;
        }
      }
    ],
    drawCallback: function (settings) {
      ocultarColumDatatableAlquilerVehiculo();
    }
  });

  tblAlquilerVehiculo.on("order.dt search.dt draw.dt", function (e, settings, processing) {
    const PageInfo = $tblAlquilerVehiculo.DataTable().page.info();
    tblAlquilerVehiculo.column(1, {search: "applied", order: "applied"})
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1 + PageInfo.start;
      });
  });

  $("#lista-alquiler-vehiculo tbody").on("click", ".details-control", function () {
    var tr = $(this).closest("tr"), row = tblAlquilerVehiculo.row(tr), datos = [];
    tr.children().each(function (item, value) {
      datos.push(value.innerText);
    });
    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
    } else {
      var dataCabecera = arrayOcultarColumaAlquilerVehiculoDatatable.map(
        (item) => `<th>${$("#lista-alquiler-vehiculo thead tr").find("th").eq(item).html()}</th>`
      );
      var dataDesc = arrayOcultarColumaAlquilerVehiculoDatatable.map((item) => `<td>${datos[item]}</td>`);
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
  $("#bs-selec-condcutor-modal-lg").on("show.bs.modal", function () {
    setTimeout(function () {
      fnTblEscogerConductor();
    }, 300);
  });

  $("#bs-selec-condcutor-modal-lg").on("hide.bs.modal", function () {
    fnTblEscConductorUncheck();
    setTimeout(function () {
      // -------------- ini -------------->>
      $("#id_alquiler_fecha_inicio").prop("disabled", false);
      $("#id_alquiler_hora_inicio").prop("disabled", false);
      $("#id_alquiler_entrega_radio").prop("disabled", false);
      $("#lista-conductores-escoger_wrapper").show()
      $("#id_alquiler_entrega_radio").prop("checked", false);
      // -------------- fin <<--------------
      fnTblAlquilerVehiculo();
      $campoBsSelectAlquilerCodigo.val("");
      $campoBsSelectVehiculoCodigo.val("");
      $campoBsSelectConductorCodigo.val("");
      $idAlquilerCampoFinalizar.prop("checked", false);
      fnAlquilarVehiculoModalRemoveManejoFechas();
    }, 300);
  });

  fnTblAlquilerVehiculo = function () {
    try {
      tblAlquilerVehiculo.search("");
      tblAlquilerVehiculo.ajax.reload(null, true);
    } catch (e) {
      console.error(e);
    }
  };
  fnTblAlquilerVehiculo();

  $("#lista-alquiler-vehiculo tbody").on("click", ".agregar-alquiler", function () {
    const $auxBtn = $(this);
    const $auxModal = $("#bs-selec-condcutor-modal-lg");
    let nombreVehiculo = $auxBtn.data("nombrevehiculo") ?? "";
    let codigoVehiculo = $auxBtn.data("codigovehiculo") ?? "";
    let codigoAlquilado = $auxBtn.data("codigoalquilado") ?? "";
    let htmlTitulo = "Agregar alquiler";
    let htmlDetalle = `Seleccionar al conductor para el vehiculo <span class="font-bold">${$auxBtn.data("nombrevehiculo") ?? ""}</span>`;
    $auxModal.find(".modal-title").html(htmlTitulo);
    $auxModal.find(".detalle-operador").html(htmlDetalle);
    $campoBsSelectAlquilerCodigo.val("");
    $campoBsSelectVehiculoCodigo.val(codigoVehiculo);
    $campoBsSelectConductorCodigo.val("");
    fnAlquilarVehiculoModalNuevoManejoFechas();
    $("#id_alquiler_entrega_radio").prop("checked", true);
    $auxModal.modal("show");
    $idAlquilerCheckOpcFinalizar.hide();
    $idAlquilerOpcInicioHoraActual.show();
  });

  $("#lista-alquiler-vehiculo tbody").on("click", ".editar-alquiler", function () {
    const $auxBtn = $(this);
    const $auxModal = $("#bs-selec-condcutor-modal-lg");
    let codigoAlquiler = $auxBtn.data("codigoalquilado") ?? "";
    const auxUrl = urlList.vehiculo.alquilerVehiculoDetail.replace("/0000/", `/${codigoAlquiler}/`);
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
        let dataConductor = data.conductor_data ?? {};
        let nombreConductor = `${dataConductor.nombre ?? ""} ${dataConductor.apellido_paterno ?? ""}`;
        let dataVehiculo = data.vehiculo_data ?? {};
        let nombreVehiculo = `${dataVehiculo.nombre ?? ""}`;
        // ------------modificar para cargar desde back ---->>
        let htmlTitulo = "Modificar alquiler";
        let htmlDetalle = `Conductor actual <span class="label label-megna">${nombreConductor}</span>
            para el vehiculo <span class="label label-megna font-bold">${nombreVehiculo}</span> <br>
            Para modificar seleccione nuevo conductor`;
        $auxModal.find(".modal-title").html(htmlTitulo);
        $auxModal.find(".detalle-operador").html(htmlDetalle);
        $campoBsSelectAlquilerCodigo.val(codigoAlquiler);
        $campoBsSelectVehiculoCodigo.val(dataVehiculo.codigo ?? "");
        $campoBsSelectConductorCodigo.val(dataConductor.codigo ?? "");
        // -- datos de formulario
        let horaInicio = (data.hora_inicio ?? "").substring(0, 5);
        $("#id_alquiler_fecha_inicio").val(data.fecha_inicio ?? "");
        $("#id_alquiler_hora_inicio").val(horaInicio);
        if (data.entrega_radio) {
          $("#id_alquiler_entrega_radio").prop("checked", true);
        } else {
          $("#id_alquiler_entrega_radio").prop("checked", false);
        }
        if (permiteModificarDataInicial === true) {
          $("#id_alquiler_fecha_inicio").prop("disabled", false);
          $("#id_alquiler_hora_inicio").prop("disabled", false);
          $("#id_alquiler_entrega_radio").prop("disabled", false);
          $("#lista-conductores-escoger_wrapper").show();
        } else {
          $("#id_alquiler_fecha_inicio").prop("disabled", true);
          $("#id_alquiler_hora_inicio").prop("disabled", true);
          $("#id_alquiler_entrega_radio").prop("disabled", true);
          $("#lista-conductores-escoger_wrapper").hide();
        }
        if (data.fecha_prog_fin) {
          $("#id_alquiler_fecha_fin").val(data.fecha_prog_fin ?? "");
        }
        if (data.hora_prog_fin) {
          $("#id_alquiler_hora_fin").val(data.hora_prog_fin ?? "");
        }
        $auxModal.modal("show");
        $idAlquilerCheckOpcFinalizar.show();
        $idAlquilerOpcInicioHoraActual.hide();
        fnAlquilarVehiculoModalModificarManejoFechas();
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

  // Delete rental handler
  $("#lista-alquiler-vehiculo tbody").on("click", ".eliminar-alquiler", function () {
    const $auxBtn = $(this);
    let codigoAlquiler = $auxBtn.data("codigoalquilado") ?? "";

    if (!codigoAlquiler) {
      swal.fire({
        title: "Error",
        html: "No se pudo obtener el código del alquiler",
        type: "error",
        showConfirmButton: true,
        confirmButtonText: "Cerrar",
      });
      return;
    }

    // Confirm deletion
    swal.fire({
      title: "¿Está seguro?",
      html: "¿Desea eliminar este alquiler permanentemente?<br><small class='text-danger'>Esta acción no se puede deshacer</small>",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar"
    }).then(function (result) {
      if (result.value) {
        const auxUrl = urlList.vehiculo.alquilerVehiculoDetail.replace("/0000/", `/${codigoAlquiler}/`);
        const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";

        $.ajax({
          url: auxUrl,
          type: "DELETE",
          dataType: "json",
          headers: {"X-CSRFToken": csrfToken},
          beforeSend: function () {
            $auxBtn.prop("disabled", true);
          },
          success: function (resp) {
            swal.fire({
              title: "Eliminado",
              html: resp.message || "El alquiler ha sido eliminado correctamente",
              type: "success",
              showConfirmButton: true,
              confirmButtonText: "Aceptar",
            }).then(function () {
              fnTblAlquilerVehiculo();
            });
          },
          error: function (error) {
            $auxBtn.prop("disabled", false);
            let errorMessage = "Error al eliminar el alquiler";
            try {
              let errorData = error.responseJSON || {};
              errorMessage = errorData.detail?.message || errorData.message || errorMessage;
            } catch (e) {
              console.error("Error parsing response:", e);
            }
            swal.fire({
              title: "Error",
              html: errorMessage,
              type: "error",
              showConfirmButton: true,
              confirmButtonText: "Cerrar",
            });
          }
        });
      }
    });
  });

  function fnAlquilarVehiculoModalRemoveManejoFechas() {
    $("#id_alquiler_fecha_inicio").val("");
    $("#id_alquiler_hora_inicio").val("");
    $("#id_alquiler_fecha_fin").val("");
    $("#id_alquiler_hora_fin").val("");
  }

  function fnAlquilarVehiculoModalModificarManejoFechas() {
    let auxFechIniActual = new Date();
    let auxFechIniMaxima = new Date();
    auxFechIniMaxima.setDate(auxFechIniMaxima.getDate() + 10);
    let fechaInicial = $("#id_alquiler_fecha_inicio").val() ?? null;
    if (!fechaInicial) {
      $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setDate", auxFechIniActual);
    }
    $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setMinDate", auxFechIniActual);
    $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setMaxDate", auxFechIniMaxima);

    let horaInicial = $("#id_alquiler_hora_inicio").val() ?? null;
    if (!horaInicial) {
      $("#id_alquiler_hora_inicio").bootstrapMaterialDatePicker("setDate", auxFechIniActual);
    } else {
      $("#id_alquiler_hora_inicio").bootstrapMaterialDatePicker("setDate", horaInicial);
    }

    let auxFechFinMaxima = new Date();
    auxFechFinMaxima.setDate(auxFechFinMaxima.getDate() + 65);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setDate", null);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setMinDate", fechaInicialActual);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setMaxDate", auxFechFinMaxima);
    $("#id_alquiler_hora_fin").bootstrapMaterialDatePicker("setDate", null);
  }

  function fnAlquilarVehiculoModalNuevoManejoFechas() {
    let auxFechIniActual = new Date();
    let auxFechIniMaxima = new Date();
    auxFechIniMaxima.setDate(auxFechIniMaxima.getDate() + 10);
    $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setDate", auxFechIniActual);
    $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setMinDate", auxFechIniActual);
    $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker("setMaxDate", auxFechIniMaxima);
    $("#id_alquiler_hora_inicio").bootstrapMaterialDatePicker("setDate", auxFechIniActual);

    let auxFechFinMaxima = new Date();
    auxFechFinMaxima.setDate(auxFechFinMaxima.getDate() + 65);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setDate", null);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setMinDate", fechaInicialActual);
    $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker("setMaxDate", auxFechFinMaxima);
    $("#id_alquiler_hora_fin").bootstrapMaterialDatePicker("setDate", null);
  }

  const fechaInicialActual = new Date();
  const fechaInicialMaxima = new Date();
  fechaInicialMaxima.setDate(fechaInicialMaxima.getDate() + 10);

  $("#id_alquiler_fecha_inicio").bootstrapMaterialDatePicker({
    format: "YYYY-MM-DD",
    time: false,
    date: true,
    lang: "es-us",
    clearButton: true,
    shortTime: false,
    clearText: "Limpiar",
    cancelText: "Cancelar",
    currentDate: fechaInicialActual,
    minDate: fechaInicialActual,
    maxDate: fechaInicialMaxima
  });
  $("#id_alquiler_hora_inicio").bootstrapMaterialDatePicker({
    format: "HH:mm", time: true, date: false, lang: "es-us",
    clearButton: true, shortTime: true,
    clearText: "Limpiar", cancelText: "Cancelar",
    currentDate: fechaInicialActual
  });

  const fechaFinlActual = new Date();
  const fechaFinMaxima = new Date();
  fechaFinMaxima.setDate(fechaFinMaxima.getDate() + 65);

  $("#id_alquiler_fecha_fin").bootstrapMaterialDatePicker({
    format: "YYYY-MM-DD",
    time: false,
    date: true,
    lang: "es-us",
    clearButton: true,
    shortTime: false,
    clearText: "Limpiar",
    cancelText: "Cancelar",
    currentDate: null,
    minDate: fechaFinlActual,
    maxDate: fechaFinMaxima
  });
  $("#id_alquiler_hora_fin").bootstrapMaterialDatePicker({
    format: "HH:mm", time: true, date: false, lang: "es-us",
    clearButton: true, shortTime: true,
    clearText: "Limpiar", cancelText: "Cancelar",
    currentDate: null
  });
  // ---------

  $btnAlquilerInicioHoraActual.click(function () {
    let auxFechIniActual = new Date();
    $("#id_alquiler_fecha_inicio").val(moment(auxFechIniActual).format("YYYY-MM-DD"));
    $("#id_alquiler_hora_inicio").val(moment(auxFechIniActual).format("HH:mm"));
    return true;
  });

  $btnAlquilerFinalizar.click(function () {
    let auxFechFinActual = new Date();
    if (!$idAlquilerCampoFinalizar.is(":checked")) {
      $idAlquilerCampoFinalizar.prop("checked", true);
    } else {
      $idAlquilerCampoFinalizar.prop("checked", false);
    }
    if ($idAlquilerCampoFinalizar.is(":checked")) {
      $("#id_alquiler_fecha_fin").val(moment(auxFechFinActual).format("YYYY-MM-DD"));
      $("#id_alquiler_hora_fin").val(moment(auxFechFinActual).format("HH:mm"));
    }
    return true;
  });
  // --------

  $btnFrmAlquilerGuardar.click(function () {
    const $auxBtnExce = $(this);
    const csrfToken = plgcliGetCookie(FRM_CSRF_TOKEN) ?? "";
    const codigoAlquiler = $campoBsSelectAlquilerCodigo.val();
    const codigoConductor = $campoBsSelectConductorCodigo.val() ?? "";
    const _data = $("#id_frm_select_alquiler :input").serializeArray();
    let auxUrl = "";
    let auxType = "PATCH";
    if (codigoAlquiler == "") {
      auxUrl = urlList.vehiculo.alquilerVehiculoList;
      auxType = "POST";
    } else {
      auxUrl = urlList.vehiculo.alquilerVehiculoDetail.replace("/0000/", `/${codigoAlquiler}/`);
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
        $("#bs-selec-condcutor-modal-lg").modal("hide");
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

  $btnFrmAlquilerCancelar.click(function () {
    $("#bs-selec-condcutor-modal-lg").modal("hide");
  });

});
