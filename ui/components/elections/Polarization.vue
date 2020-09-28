<template>
  <div>
    <h2 class="text-center pa-4">Polarização entre seguidores de candidatos</h2>
    <v-card
      class="ma-2"
      elevation="10"
      :loading="loading_plot ? 'primary' : false"
    >
      <h3 class="text-center pa-4">
        Análise da semelhança entre os seguidores dos diferentes candidatos
      </h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Esta tabela mostra o
        <a href="https://en.wikipedia.org/wiki/Jaccard_index">Jaccard Index</a>
        (JI) para cada par de conjuntos de seguidores no Twitter, entre os
        diferentes candidatos. Valores mais altos implicam que há uma maior
        semelhança entre os conjuntos. Se dois candidatos tiverem exatamente os
        mesmos seguidores, o valor de JI entre eles é 1. Esta é uma possível
        métrica que indica a polarização entre seguidores, sendo que se espera
        que candidatos que apelem aos mesmos utilizadores, tenham um índice
        maior. <br />
      </p>
      <div id="followers_polatization_heatmap"></div>
    </v-card>
    <br />
    <v-card
      class="ma-2"
      elevation="10"
      :loading="loading_plot ? 'primary' : false"
    >
      <h3 class="text-center pa-4">Análise da interseção de utilizadores</h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Por outro lado, esta tabela permite responder à questão: Que percentagem
        dos seguidores de um candidato seguem outro. Neste caso, que percentagem
        de seguidores do candidato numa dada linha seguem o candidato de uma
        dada coluna. Naturalmente, exclui-se a diagonal por esse valor ser
        sempre 1, já que cada candidato partilha todos os seguidores consigo
        mesmo :)
      </p>
      <div id="followers_ratios_heatmap"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "measure followers polarization" },
    });

    // this.date = r.data.history[0][0]; //only contains this date
    this.candidates = r.data.history[1][0].candidates;
    this.polarization = r.data.history[1][0].polarization;
    this.ratios = r.data.history[1][0].ratios;
    this.x = this.candidates.map((c) => `#${c[0]}`);

    this.display();
  },
  data() {
    return {
      candidates: [],
      polarization: [],
      ratios: [],
      loading_plot: false,
    };
  },
  methods: {
    displayPolarization() {
      this.polarization = this.polarization.map((row) =>
        row.map((cell) => cell.toFixed(4))
      );
      let data = [
        {
          z: this.polarization,
          x: this.x,
          y: this.x,
          type: "heatmap",
          hoverongaps: false,
          colorscale: "YlGnBu",
          colorscale: [
            [0, "#fff"],
            [1, "#06CDF4"],
          ],
          showscale: false,
        },
      ];
      let layout = {
        title: "Semelhança entre os conjuntos de seguidores (Jaccard Index)",
        annotations: [],
        xaxis: {
          ticks: "",
          side: "top",
        },
        yaxis: {
          ticks: "",
          ticksuffix: " ",
          width: 700,
          height: 700,
          autosize: false,
          autorange: "reversed",
        },
        height: 650,
        margin: {
          t: 150,
          l: 150,
        },
      };

      for (let i = 0; i < this.x.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          let currentValue = this.polarization[i][j];
          let textColor = currentValue > 0 ? "black" : "white";
          let result = {
            xref: "x1",
            yref: "y1",
            x: this.x[j],
            y: this.x[i],
            text: this.polarization[i][j],
            font: {
              family: "Roboto",
              size: 12,
              color: textColor,
            },
            showarrow: false,
          };
          layout.annotations.push(result);
        }
      }

      Plotly.newPlot("followers_polatization_heatmap", data, layout);
    },
    displayRatios() {
      this.ratios = this.ratios.map((row) =>
        row.map((cell) => (cell * 100).toFixed(2))
      );
      let data = [
        {
          z: this.ratios,
          x: this.x,
          y: this.x,
          type: "heatmap",
          hoverongaps: false,
          colorscale: "YlGnBu",
          colorscale: [
            [0, "#fff"],
            [1, "#06CDF4"],
          ],
          showscale: false,
        },
      ];
      let layout = {
        title:
          "Percentagem de seguidores de Candidato linha que seguem candidato coluna",
        annotations: [],
        xaxis: {
          ticks: "",
          side: "top",
        },
        yaxis: {
          ticks: "",
          ticksuffix: " ",
          width: 700,
          height: 700,
          autosize: true,
          autorange: "reversed",
        },
        height: 650,
        margin: {
          t: 150,
          l: 150,
        },
      };

      for (let i = 0; i < this.x.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          let currentValue = this.ratios[i][j];
          let textColor = currentValue > 0 ? "black" : "white";
          let result = {
            xref: "x1",
            yref: "y1",
            x: this.x[j],
            y: this.x[i],
            text: this.ratios[i][j],
            font: {
              family: "Roboto",
              size: 12,
              color: textColor,
            },
            showarrow: false,
          };
          layout.annotations.push(result);
        }
      }

      Plotly.newPlot("followers_ratios_heatmap", data, layout);
    },
    display() {
      this.displayPolarization();
      this.displayRatios();
      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
