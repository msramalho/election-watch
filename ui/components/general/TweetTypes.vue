<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h2 class="text-center pa-4">Tipos de Tweets ao longo do tempo</h2>
      <div id="types_of_tweets_totals"></div>
      <div id="types_of_tweets_percent"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "count by type" },
    });

    this.x = r.data.history[0].map((d) => new Date(d));
    this.y = r.data.history[1];

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
      let options = {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      };
      let traces = [
        {
          x: this.x,
          y: this.y.map((x) => x.reply),
          stackgroup: "one",
          name: "#replies",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.quote),
          stackgroup: "one",
          name: "#quotes",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.retweet),
          stackgroup: "one",
          name: "#retweets",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.original),
          stackgroup: "one",
          name: "#originals",
        },
      ];
      Plotly.newPlot("types_of_tweets_totals", traces, {
        ...options,
        title: "Valores totais",
      });

      let traces2 = JSON.parse(JSON.stringify(traces));
      traces2[0].groupnorm = "percent";
      Plotly.newPlot("types_of_tweets_percent", traces2, {
        ...options,
        title: "Valores normalizados",
      });
      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
