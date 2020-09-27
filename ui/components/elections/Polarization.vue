<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <p class="pa-5">lorem</p>
      <h2 class="text-center pa-4">Contas por ano e mês de criação</h2>
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
    display() {
      this.x = this.candidates.map((c) => `#${c[0]}`);
      this.heatmap_polarization = this.heatmap_polarization.map((row) =>
        row.map((cell) => (cell == 1 ? undefined : cell.toFixed(4)))
      );
      let data = [
        {
          z: this.heatmap_polarization,
          x: this.x,
          y: this.x,
          type: "heatmap",
          hoverongaps: false,
          colorscale: "YlGnBu",
          //   colorscale: [
          //     [0, "#000"],
          //     [1, "#fff"],
          //   ],
          showscale: false,
        },
      ];
      let layout = {
        title: "Annotated Heatmap",
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
      };

      for (let i = 0; i < this.x.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          let currentValue = this.heatmap_polarization[i][j];
          let textColor = currentValue > 0.1 ? "black" : "white";
          let result = {
            xref: "x1",
            yref: "y1",
            x: this.x[j],
            y: this.x[i],
            text: this.heatmap_polarization[i][j],
            font: {
              family: "Arial",
              size: 12,
              color: "rgb(50, 171, 96)",
            },
            showarrow: false,
            font: {
              color: textColor,
            },
          };
          layout.annotations.push(result);
        }
      }

      Plotly.newPlot("followers_polatization_heatmap", data, layout);

      //   let traces = [
      //     {
      //       x: this.x,
      //       y: this.y,
      //       stackgroup: "one",
      //       name: "#contas",
      //     },
      //   ];
      //   Plotly.newPlot("followers_polatization_heatmap", traces, {
      //     colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      //   });

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
