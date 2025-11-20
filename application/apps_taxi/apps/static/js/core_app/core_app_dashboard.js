$(document).ready(function () {
  const dataReport = JSON.parse($("#dataJsonSpark").text());

  function fnGraficar() {
    const prekeyLlamadas = "sparklinedash_llamada_";
    const prekeyRegistrados = "sparklinedash_registrada_";
    const prekeyAsignados = "sparklinedash_asignada_";
    let _htmlLlamadas = [];
    let _htmlRegistrados = [];
    let _htmlAsignados = [];
    let datRepo = dataReport ?? [];
    datRepo.forEach(function (item, key) {
      let operador = item.operador ?? {};
      let nombre = `${operador.nombre ?? ""} ${operador.apellido_paterno ?? ""}`;
      let codigo = operador.codigo ?? "";
      _htmlLlamadas.push(`
      <div class="col-lg-3 m-b-30 text-center text-black-50">
        <div class="m-10" style="background: #fb967810 !important;">
          <small> ${codigo} </small>
          <h2><i class="ti-arrow-up text-primary"></i> ${nombre}</h2>
          <div id="${prekeyLlamadas}${key}"></div>
          <div>${item.llamadas_atendidos ?? "-"}</div>
        </div>
      </div>`);
      _htmlRegistrados.push(`
      <div class="col-lg-3 m-b-30 text-center text-black-50">
        <div class="m-10" style="background: #038fcd10 !important;">
          <small> ${codigo} </small>
          <h2><i class="ti-arrow-up text-info"></i> ${nombre}</h2>
          <div id="${prekeyRegistrados}${key}"></div>
          <div>${item.servicios_registradas ?? "-"}</div>
        </div>
      </div>`);
      _htmlAsignados.push(`
      <div class="col-lg-3 m-b-30 text-center text-black-50">
        <div class="m-10" style="background: #009c7510 !important;">
          <small> ${codigo} </small>
          <h2><i class="ti-arrow-up text-success"></i> ${nombre}</h2>
          <div id="${prekeyAsignados}${key}"></div>
          <div>${item.servicios_asignadas ?? "-"}</div>
        </div>
      </div>`);
    });

    $("#viewJsonSparkGraficarLlamadas").html(_htmlLlamadas.join(""));
    $("#viewJsonSparkGraficarRegistrados").html(_htmlRegistrados.join(""));
    $("#viewJsonSparkGraficarAsignados").html(_htmlAsignados.join(""));

    setTimeout(function () {
      datRepo.forEach(function (item, key) {
        let dataLlamdas = ((item.llamadas_atendidos ?? "0").split(",")).map((item) => parseInt(item));
        let $grafIdGrafLlamadas = $(`#${prekeyLlamadas}${key}`);
        $grafIdGrafLlamadas.sparkline(dataLlamdas, {
          type: "bar",
          height: "50",
          barWidth: "4",
          resize: true,
          barSpacing: "10",
          barColor: "#f96262"
        });
        let dataRegistradas = ((item.servicios_registradas ?? "0").split(",")).map((item) => parseInt(item));
        let $grafIdGrafRegistradas = $(`#${prekeyRegistrados}${key}`);
        $grafIdGrafRegistradas.sparkline(dataRegistradas, {
          type: "bar",
          height: "50",
          barWidth: "4",
          resize: true,
          barSpacing: "10",
          barColor: "#03a9f3"
        });
        let dataAsignadas = ((item.servicios_asignadas ?? "0").split(",")).map((item) => parseInt(item));
        let $grafIdGrafAsignadas = $(`#${prekeyAsignados}${key}`);
        $grafIdGrafAsignadas.sparkline(dataAsignadas, {
          type: "bar",
          height: "50",
          barWidth: "4",
          resize: true,
          barSpacing: "10",
          barColor: "#4caf50"
        });

      });
    }, 350);

  }

  fnGraficar();

});
