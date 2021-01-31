<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">{{ $t("general.tweet_types.title") }}</h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="$t('general.tweet_types.explanation')"
      ></p>
      <h3 class="mb-0 pb-0">{{ $t("general.tweet_types.plot_1_title") }}</h3>
      <div id="types_of_tweets_totals"></div>
      <br />
      <h3 class="mb-0 pb-0">{{ $t("general.tweet_types.plot_2_title") }}</h3>
      <div id="types_of_tweets_percent"></div>

      <h3 class="text-center pa-4">
        {{ $t("general.tweet_types.statistics.title") }}
      </h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        <v-simple-table>
          <thead>
            <tr>
              <td>
                {{ $t("general.tweet_types.statistics.col_stats.title") }}
              </td>
              <td>
                {{ $t("general.tweet_types.statistics.col_values.title") }}
              </td>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {{
                  $t("general.tweet_types.statistics.col_stats.total_start") +
                  x.length +
                  $t("general.tweet_types.statistics.col_stats.total_end")
                }}
              </td>
              <td>{{ sum(daily).toLocaleString() }}</td>
            </tr>
            <tr>
              <td>{{ $t("general.tweet_types.statistics.col_stats.avg") }}</td>
              <td>
                {{ parseInt(sum(daily) / daily.length).toLocaleString() }}
              </td>
            </tr>
            <tr>
              <td>{{ $t("general.tweet_types.statistics.col_stats.max") }}</td>
              <td>{{ max(daily).toLocaleString() }}</td>
            </tr>
            <tr>
              <td>{{ $t("general.tweet_types.statistics.col_stats.min") }}</td>
              <td>{{ min(daily).toLocaleString() }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </p>
      <br />
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    // const r = await this.$axios.get(`task_data`, {params: { task_name: "count by type" },});
    const r = await this.$axios.get(`task_data_count_by_type.json`);

    this.x = r.data.history[0].map((d) => new Date(d));
    this.y = r.data.history[1];
    this.daily = this.y.map((day) => day.total);

    this.display();
  },
  data() {
    return {
      x: [],
      y: [],
      daily: [],
      logs: { time: [] },
      loading_plot: false,
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },
    max(arr) {
      if (!arr.length) return 0;
      return arr.reduce((a, b) => Math.max(a, b), arr[0]);
    },
    min(arr) {
      if (!arr.length) return 0;
      return arr.reduce((a, b) => Math.min(a, b), arr[0]);
    },
    display() {
      let options = {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      };
      let traces = [
        {
          x: this.x,
          y: this.y.map((x) => x.reply),
          stackgroup: "one",
          name: "replies",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.quote),
          stackgroup: "one",
          name: "quotes",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.retweet),
          stackgroup: "one",
          name: "retweets",
        },
        {
          x: this.x,
          y: this.y.map((x) => x.original),
          stackgroup: "one",
          name: "originals",
        },
      ];
      Plotly.newPlot("types_of_tweets_totals", traces, {
        ...options,
        // title: this.$i18n.t("general.tweet_types.plot_1_title"),
      });

      let traces2 = JSON.parse(JSON.stringify(traces));
      traces2[0].groupnorm = "percent";
      Plotly.newPlot("types_of_tweets_percent", traces2, {
        ...options,
        // title: this.$i18n.t("general.tweet_types.plot_2_title"),
      });
      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
