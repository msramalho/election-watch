<template>
  <div>
    <br />
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">{{ $t("general.creation_dates.title") }}</h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="$t('general.creation_dates.explanation')"
      ></p>
      <div id="users_by_creation_date"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    // const r = await this.$axios.get(`task_data`, {params: { task_name: "measure creation dates" },});
    const r = await this.$axios.get(`task_data_measure_creation_dates.json`);

    this.date = r.data.history[0][0]; //only contains this date
    this.data_points = r.data.history[1][0].filter(
      (dp) => dp.year !== null && dp.year != 1970
    );
    this.x = this.data_points.map((dp) => new Date(dp.year, dp.month - 1, 1));
    this.y = this.data_points.map((dp) => dp.count);

    this.display();
  },
  data() {
    return {
      x: [],
      y: [],
      logs: { time: [] },
      loading_plot: false,
    };
  },
  methods: {
    display() {
      let traces = [
        {
          x: this.x,
          y: this.y,
          stackgroup: "one",
          name: "#contas",
        },
      ];
      Plotly.newPlot("users_by_creation_date", traces, {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      });

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
