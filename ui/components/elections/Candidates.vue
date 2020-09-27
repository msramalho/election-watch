<template>
  <div>
    <!-- <v-card class="ma-4 my-10" :loading="loading_plot ? 'primary' : false"> -->
    <h2 class="text-center pa-4">Análise Candidatos</h2>
    <p class="pa-4">Nos últimos {{ x.length }} dias</p>

    <v-progress-circular
      :size="50"
      indeterminate
      color="primary"
      v-if="loading_plot ? 'primary' : false"
      class="my-10"
    ></v-progress-circular>

    <div id="mentions_over_time_all"></div>
    <div id="tweet_impact_over_time_all"></div>

    <v-expansion-panels class="mb-10" popout>
      <v-expansion-panel
        v-for="(candidate, i) in candidateNames"
        :key="i"
        @click="displayCandidate(candidate, i)"
      >
        <v-expansion-panel-header>
          {{ candidate }}
          <v-spacer></v-spacer>

          <v-btn
            :href="`https://twitter.com/${candidates[candidate].metrics[0].screen_name}`"
            icon
            color="primary"
            rounded
            max-width="150px"
          >
            <v-icon>mdi-twitter</v-icon>&nbsp; perfil
          </v-btn>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="text-left">
          Neste momento, {{ candidate }} tem
          <strong>{{
            candidates[candidate].metrics[0].followers_count.toLocaleString()
          }}</strong>
          seguidores.
          <br />
          Nos últimos {{ x.length }} dias, publicou
          {{ sum(candidates[candidate].metrics.map((m) => m.tweets.length)) }}
          tweets ({{
            sum(
              candidates[candidate].metrics.map(
                (x) => x.tweets.filter((t) => t.type == "original").length
              )
            ).toLocaleString()
          }}
          originais,
          {{
            sum(
              candidates[candidate].metrics.map(
                (x) => x.tweets.filter((t) => t.type == "retweet").length
              )
            ).toLocaleString()
          }}
          retweets,
          {{
            sum(
              candidates[candidate].metrics.map(
                (x) => x.tweets.filter((t) => t.type == "reply").length
              )
            ).toLocaleString()
          }}
          replies,
          {{
            sum(
              candidates[candidate].metrics.map(
                (x) => x.tweets.filter((t) => t.type == "quote").length
              )
            ).toLocaleString()
          }}
          quotes).
          <br />
          Criando um impacto total (likes+retweets) de
          {{
            sum(
              candidates[candidate].metrics.map((x) => x.tweet_impact)
            ).toLocaleString()
          }}
          ({{
            (
              sum(candidates[candidate].metrics.map((z) => z.tweet_impact)) /
              x.length
            ).toLocaleString()
          }}
          por dia).
          <!-- {{ candidates[candidate] }} -->

          <!-- <div :id="`performance_over_time_${candidates[candidate]._id}`"></div> -->
          <div :id="`mentions_over_time_${i}`"></div>
          <div :id="`tweet_impact_over_time_${i}`"></div>
          <div :id="`followers_over_time_${i}`"></div>

          <v-data-table
            :headers="tableHeaders"
            :items="candidates[candidate].metrics.map((x) => x.tweets).flat()"
            item-key="_id"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>Tweets {{ candidate }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <!-- <v-text-field
                  v-model="candidates[candidate].search"
                  append-icon="mdi-magnify"
                  label="Pesquisar"
                  single-line
                  hide-details
                ></v-text-field> -->
              </v-toolbar>
            </template>
          </v-data-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <br />
    <!-- </v-card> -->
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "measure candidates" },
    });

    // read relevant data
    this.x = r.data.history[0].map((d) => new Date(d)).reverse();
    // this.totals = r.data.history[1].map((x) => x.total).reverse();
    this.candidates = {};
    r.data.history[1].forEach((list, i) => {
      // this.candidates[candidate]
      let _ids = Object.keys(list.candidates);
      _ids.forEach((_id) => {
        let name = list.candidates[_id].name;
        if (this.candidates[name] === undefined)
          this.candidates[name] = { _id, metrics: [], search: "" };
        this.candidates[name].metrics.push(list.candidates[_id]);
      });
    });
    this.candidateNames = Object.keys(this.candidates);
    this.candidateNames.sort();
    console.log(this.candidates);
    this.display();
    this.loading_plot = false;
  },
  data() {
    return {
      x: [],
      totals: [],
      loading_plot: false,
      candidateNames: [],
      tableHeaders: [
        { text: "ID", value: "_id", align: "center" },
        { text: "Tipo", value: "type", align: "center" },
        { text: "Texto", value: "full_text", align: "center" },
        { text: "Likes", value: "favorite_count", align: "center" },
        { text: "Retweets", value: "retweet_count", align: "center" },
        // { text: "", value: "data-table-expand" },
      ],
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },
    max(arr) {
      return arr.reduce((a, b) => Math.max(a, b));
    },
    display() {
      let tracesMentions = this.candidateNames.map((cname, i) => {
        let c = this.candidates[cname];
        return {
          x: this.x,
          y: c.metrics.map((m) => m.name_mentions + m.mentions),
          type: "scatter",
          mode: "lines+markers",
          name: `menções ${cname}`,
        };
      });
      Plotly.newPlot(`mentions_over_time_all`, tracesMentions, {
        colorway: [
          "EF7B45",
          "4F6D7A",
          "16DB65",
          "947BD3",
          "0CAADC",
          "5eb1bf",
          "cdedf6",
          "ef7b45",
          "d84727",
          "fffd98",
        ],
        title: `Menções ao longo do tempo`,
      });
      let tracesImpact = this.candidateNames.map((cname, i) => {
        let c = this.candidates[cname];
        return {
          x: this.x,
          y: c.metrics.map((m) => m.tweet_impact),
          type: "scatter",
          mode: "lines+markers",
          name: `impacto ${cname}`,
        };
      });
      Plotly.newPlot(`tweet_impact_over_time_all`, tracesImpact, {
        colorway: [
          "EF7B45",
          "4F6D7A",
          "16DB65",
          "947BD3",
          "0CAADC",
          "5eb1bf",
          "cdedf6",
          "ef7b45",
          "d84727",
          "fffd98",
        ],
        title: `Impacto ao longo do tempo (likes+retweets)`,
      });
    },
    displayCandidate(cname, i) {
      setTimeout(() => {
        let c = this.candidates[cname];
        let followers_count = c.metrics.map((x) => x.followers_count);
        let name_mentions = c.metrics.map((x) => x.name_mentions);
        let mentions = c.metrics.map((x) => x.mentions);
        let tweet_impact = c.metrics.map((x) => x.tweet_impact);
        let tweet_count = c.metrics.map((x) => x.tweets.length);
        let tweet_count_original = c.metrics.map(
          (x) => x.tweets.filter((t) => t.type == "original").length
        );
        let options = {
          colorway: ["EF7B45", "4F6D7A", "16DB65", "947BD3", "0CAADC"],
        };
        Plotly.newPlot(
          `mentions_over_time_${i}`,
          [
            {
              x: this.x,
              y: name_mentions,
              type: "scatter",
              mode: "lines+markers",
              name: `menções '${cname}'`,
            },
            {
              x: this.x,
              y: mentions,
              type: "scatter",
              mode: "lines+markers",
              name: `menções '@${c.metrics[0].screen_name}'`,
            },
          ],
          { ...options, title: `Menções ao longo do tempo para ${cname}` }
        );
        Plotly.newPlot(
          `followers_over_time_${i}`,
          [
            {
              x: this.x,
              y: followers_count,
              type: "scatter",
              mode: "lines+markers",
              name: "seguidores",
            },
          ],
          { ...options, title: `Seguidores ao longo do tempo para ${cname}` }
        );
        Plotly.newPlot(
          `tweet_impact_over_time_${i}`,
          [
            {
              x: this.x,
              y: tweet_impact,
              type: "scatter",
              mode: "lines+markers",
              name: "impacto",
            },
            {
              x: this.x,
              y: tweet_count,
              type: "scatter",
              mode: "lines+markers",
              name: "#tweets totais",
              yaxis: "y2",
            },
            {
              x: this.x,
              y: tweet_count_original,
              type: "scatter",
              mode: "lines+markers",
              name: "#tweets originais",
              yaxis: "y2",
            },
          ],
          {
            ...options,
            yaxis: { title: "impacto diário" },
            yaxis2: {
              title: "tweets diários",
              overlaying: "y",
              side: "right",
            },
            title: `Tweets e impacto (likes+retweets) para ${cname}`,
          }
        );
      }, 200);
    },
  },
  fetchOnServer: false,
};
</script>
