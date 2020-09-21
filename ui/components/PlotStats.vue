<template>
  <!-- <div v-if="logs.time.length"> -->
  <div>
    <h3 class="ma-4">
      Total points: {{logs.time.length}}
      <small
        v-if="logs.last_updated"
      >(last updated: {{logs.last_updated}})</small>
    </h3>
    <v-card class="ma-2" :loading="loading_user_tweets?'primary':false">
      <h2 class="text-center pa-4">Tweets and Users over time</h2>
      <div id="scatter_users_tweets"></div>
    </v-card>
    <v-card class="ma-2" :loading="loading_mb?'primary':false">
      <h2 class="text-center pa-4">Database size over time</h2>
      <div id="scatter_mb"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_user_tweets = true;
    this.loading_mb = true;
    const r = await this.$axios.get(`db_logs`, {
      // params: { max_items: 500 },
    });
    r.data.last_updated = new Date(
      Date.parse(r.data.last_updated)
    ).toLocaleTimeString();
    this.logs = r.data;
    this.display();
  },
  data() {
    return {
      logs: { time: [] },
      loading_user_tweets: false,
      loading_mb: false,
    };
  },
  methods: {
    display() {
      let trace_users = {
        x: this.logs.time,
        y: this.logs.users,
        mode: "markers",
        name: "#users",
        type: "scatter",
      };
      let trace_tweets = {
        x: this.logs.time,
        y: this.logs.tweets,
        mode: "markers",
        name: "#tweets",
        type: "scatter",
      };

      Plotly.newPlot("scatter_users_tweets", [trace_users, trace_tweets]);
      this.loading_user_tweets = false;

      // size scatter
      let trace_mb = {
        x: this.logs.time,
        y: this.logs.mb,
        mode: "markers",
        name: "size (MB)",
        type: "scatter",
      };
      Plotly.newPlot("scatter_mb", [trace_mb]);
      this.loading_mb = false;
    },
  },
  fetchOnServer: false,
};
</script>
