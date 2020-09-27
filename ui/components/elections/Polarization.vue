<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h2 class="text-center pa-4">
        Polarização entre seguidores de candidatos
      </h2>
      <p class="pa-5">
        Esta tabela mostra o
        <a href="https://en.wikipedia.org/wiki/Jaccard_index">Jaccard Index</a>
        (JI) para cada par de conjunto de seguidores no Twitter, entre os
        diferentes candidatos.<br />
        Valores mais altos implicam que há uma maior semelhança entre os
        conjuntos. Se as mesmas contas seguirem dois candidatos, o valor de JI
        entre eles é 1.
      </p>
      <div id="followers_polatization_heatmap"></div>
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
    this.heatmap_polarization = r.data.history[1][0].polarization_matrix;

    console.log(this.heatmap_polarization);
    // this.data_points = r.data.history[1][0].filter(
    //   (dp) => dp.year !== null && dp.year != 1970
    // );
    // this.x = this.data_points.map((dp) => new Date(dp.year, dp.month - 1, 1));
    // this.y = this.data_points.map((dp) => dp.count);

    this.display();
  },
  data() {
    return {
      candidates: [],
      heatmap_polarization: [],
      loading_plot: false,
    };
  },
  methods: {
    max(arr) {
      return arr.reduce((a, b) => Math.max(a, b));
    },
    display() {
      this.x = this.candidates.map((c) => `#${c[0]}`);
      this.heatmap_polarization = this.heatmap_polarization.map((row) =>
        row.map((cell) => (cell == 1 ? undefined : cell.toFixed(4)))
      );
      let max = this.max(this.heatmap_polarization.flat());
      let data = [
        {
          z: this.heatmap_polarization,
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
          t: 200,
          l: 150,
        },
      };

      for (let i = 0; i < this.x.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          let currentValue = this.heatmap_polarization[i][j];
          //   let textColor = currentValue >= max ? "black" : "white";
          let textColor = currentValue > 0 ? "black" : "white";
          let result = {
            xref: "x1",
            yref: "y1",
            x: this.x[j],
            y: this.x[i],
            text: this.heatmap_polarization[i][j],
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

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
