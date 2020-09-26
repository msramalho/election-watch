<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h2 class="text-center pa-4">Notícias Falsas</h2>
      <p class="pa-4">
        Nos últimos {{ x.length }} dias, foram partilhados um total de
        <strong>{{ sum(totals) }} tweets</strong>
        contendo links para sites de notícias falsas.

        <br />Estes tweets receberam um total de {{ sum(favourite_counts) }}
        <i>likes</i> (média:
        {{ sum(favourite_counts) / sum(totals) }} likes/tweet) e
        {{ sum(retweet_counts) }} <i>retweets</i> (média:
        {{ sum(retweet_counts) / sum(totals) }} retweets/tweet).

        <br />Neste momento, estamos a monitorizar
        <strong>{{ sites.length }}</strong> websites e páginas de facebook de
        notícias falsas.
      </p>
      <div id="fakenews_over_time"></div>
      <div id="fakenews_by_website_more_than_5"></div>
      <div id="fakenews_by_website_grouped"></div>
      <!-- <div id="fakenews_by_website_heatmap"></div> -->
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "measure fakenews" },
    });

    // console.log(r.data);
    // read relevant data
    this.x = r.data.history[0].map((d) => new Date(d));
    this.totals = r.data.history[1].map((x) => x.total);
    this.favourite_counts = r.data.history[1].map((x) => x.favourite_count);
    this.retweet_counts = r.data.history[1].map((x) => x.retweet_count);

    this.sites = Object.keys(r.data.history[1][0].sites).map((site) =>
      site.replace("-", ".")
    );

    //heatmap
    let n = this.sites.length;
    this.heatmap = [];
    for (let i = 0; i < n; i++) {
      this.heatmap[i] = [];
      for (let j = 0; j < this.x.length; j++) {
        this.heatmap[i][j] = 0;
      }
    }
    // this.heatmap = new Array(n).fill(new Array(this.x.length));
    r.data.history[1].forEach((day, i) => {
      Object.entries(day.sites).forEach((site, j) => {
        this.heatmap[j][i] = site[1];
      });
    });

    this.display();
  },
  data() {
    return {
      x: [],
      totals: [],
      heatmap: [],
      sites: [],
      last_updated: false,
      logs: { time: [] },
      loading_plot: false,
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },

    display() {
      let options = {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      };
      let traces = [
        {
          x: this.x,
          y: this.totals,
          type: "scatter",
          mode: "lines+markers+text",
          text: this.totals,
          textposition: "top",
          name: "notícias falsas",
        },
      ];
      Plotly.newPlot("fakenews_over_time", traces, {
        ...options,
        title: "Notícias Falsas por dia",
      });

      //lineplots
      let tracesLines = this.heatmap.map((siteData, i) => {
        if (siteData.every((item) => item < 5)) return {};
        return {
          x: this.x,
          y: siteData,
          mode: "lines",
          name: this.sites[i],
        };
      });
      let layoutLines = {
        title:
          "Partilhas por site do notícias falsas, <br>filtrado para mínimo de 5 num dos dias",
        height: 500,
        colorway: [
          "16DB65",
          "947BD3",
          "0CAADC",
          "EF7B45",
          "4F6D7A",
          "042a2b",
          "5eb1bf",
          "cdedf6",
          "ef7b45",
          "d84727",
          "fffd98",
        ],
      };
      Plotly.newPlot(
        "fakenews_by_website_more_than_5",
        tracesLines,
        layoutLines
      );

      // grouped
      let traceGrouped = {
        x: this.sites,
        y: this.heatmap.map((siteData) => this.sum(siteData)),
        type: "bar",
        text: this.sites,
        marker: {
          color: "rgba(58,200,225,.5)",
        },
        transforms: [
          {
            type: "sort",
            target: "y",
            order: "descending",
          },
          { type: "filter", target: "y", operation: ">", value: 0 },
        ],
      };

      let layout = {
        title: `Notícias falsas partilhadas, valor total por site nos últimos ${this.x.length} dias`,
        showlegend: false,
        xaxis: {
          tickangle: -45,
        },
        yaxis: {
          zeroline: false,
          gridwidth: 2,
        },
        bargap: 0.05,
        height: 650,
        margin: {
          b: 250,
        },
      };

      Plotly.newPlot("fakenews_by_website_grouped", [traceGrouped], layout);

      // heatmap
      // let heatData = [
      //   {
      //     z: this.heatmap,
      //     type: "heatmap",
      //     y: this.sites,
      //     colorscale: "YlGnBu",
      //   },
      // ];
      // Plotly.newPlot("fakenews_by_website_heatmap", heatData);

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
