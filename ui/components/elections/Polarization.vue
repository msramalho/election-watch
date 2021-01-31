<template>
  <div>
    <h2 class="text-center pa-4">{{ $t("elections.polarization.title") }}</h2>
    <v-card
      class="ma-2"
      elevation="10"
      :loading="loading_plot ? 'primary' : false"
    >
      <h3 class="text-center pa-4">
        {{ $t("elections.polarization.similarity.title") }}
      </h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="$t('elections.polarization.similarity.description')"
      ></p>
      <h3 class="mb-0 pb-0 mx-auto">
        {{ $t("elections.polarization.similarity.plot_title") }}
      </h3>
      <div id="followers_polatization_heatmap"></div>
    </v-card>
    <br />
    <v-card
      class="ma-2"
      elevation="10"
      :loading="loading_plot ? 'primary' : false"
    >
      <h3 class="text-center pa-4">
        {{ $t("elections.polarization.intersection.title") }}
      </h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="$t('elections.polarization.intersection.description')"
      ></p>
      <h3 class="mb-0 pb-0 mx-auto">
        {{ $t("elections.polarization.intersection.plot_title") }}
      </h3>
      <div id="followers_ratios_heatmap"></div>
    </v-card>
    <br />
    <v-card
      class="ma-2"
      elevation="10"
      :loading="loading_plot ? 'primary' : false"
    >
      <h3 class="text-center pa-4">
        {{ $t("elections.polarization.radar.title") }}
      </h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="$t('elections.polarization.radar.description')"
      ></p>
      <h3 class="mb-0 pb-0 mx-auto">
        {{ $t("elections.polarization.radar.plot_title") }}
      </h3>
      <div id="followers_ratios_radar"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    // const r = await this.$axios.get(`task_data`, {params: { task_name: "measure followers polarization" },});
    const r = await this.$axios.get(
      `task_data_measure_followers_polarization.json`
    );

    // this.date = r.data.history[0][0]; //only contains this date
    this.candidates = r.data.history[1][0].candidates;
    this.polarization = r.data.history[1][0].polarization;
    this.ratios = r.data.history[1][0].ratios;
    this.x = this.candidates.map((c) => `@${c[0]}`);

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
    max(arr) {
      return arr.reduce((a, b) => Math.max(a, b));
    },
    transpose(matrix) {
      return matrix[0].map((_, colIndex) => matrix.map((row) => row[colIndex]));
    },
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
        // title: "Semelhança entre os conjuntos de seguidores (Jaccard Index)",
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
      let ratios = this.ratios.map((row) =>
        row.map((cell) => (cell * 100).toFixed(2))
      );
      let data = [
        {
          z: ratios,
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
        // title: "Percentagem de seguidores de Candidat@ linha que seguem Candidat@ coluna",
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
          let currentValue = ratios[i][j];
          let textColor = currentValue > 0 ? "black" : "white";
          let result = {
            xref: "x1",
            yref: "y1",
            x: this.x[j],
            y: this.x[i],
            text: ratios[i][j],
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
    displayRatiosRadar() {
      let ratios = this.ratios.map((row, i) => {
        row[i] = 1;
        return row;
      });
      ratios = this.transpose(ratios);
      let candidateNames = this.candidates.map((c) => c[0]);
      let data = this.candidates.map((c, i) => {
        return {
          type: "scatterpolar",
          r: ratios[i],
          theta: candidateNames,
          fill: "toself",
          name: candidateNames[i],
          closedTrace: true,
        };
      });

      let layout = {
        // title: "Visualização em radar da interseção de seguidores",
        polar: {
          radialaxis: {
            visible: true,
            range: [0, this.max(this.ratios.flat())],
          },
        },
        autosize: true,
        // width: 500,
        height: 600,
      };

      Plotly.newPlot("followers_ratios_radar", data, layout);
    },
    display() {
      this.displayPolarization();
      this.displayRatios();
      this.displayRatiosRadar();
      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
