<template>
  <div>
    <!-- <v-card class="ma-4 my-10" :loading="loading_plot ? 'primary' : false"> -->
    <v-card class="ma-2" elevation="10">
      <h3 class="text-center pa-4" v-html="$t('elections.mentions.title')"></h3>
      <small> {{ $t("elections.mentions.details") }}</small>
      <v-progress-circular
        :size="50"
        indeterminate
        color="primary"
        v-if="loading_plot ? 'primary' : false"
        class="my-10"
      ></v-progress-circular>

      <div id="mentions_over_time_all"></div>
    </v-card>
    <br />
    <v-card class="ma-2" elevation="10">
      <h3 class="text-center pa-4" v-html="$t('elections.impact.title')"></h3>
      <v-progress-circular
        :size="50"
        indeterminate
        color="primary"
        v-if="loading_plot ? 'primary' : false"
        class="my-10"
      ></v-progress-circular>
      <div id="tweet_impact_over_time_all"></div>
    </v-card>
    <br />

    <br />
    <v-card class="ma-2" elevation="10">
      <h3 class="text-center pa-4">
        {{ $t("elections.followers.title") }}
      </h3>
      <small> {{ $t("elections.followers.note") }}</small>
      <v-progress-circular
        :size="50"
        indeterminate
        color="primary"
        v-if="loading_plot ? 'primary' : false"
        class="my-10"
      ></v-progress-circular>
      <div id="followers_over_time_all"></div>
    </v-card>
    <br />

    <br />
    <v-card class="ma-2" elevation="10">
      <h3
        class="text-center pa-4"
        v-html="$t('elections.hatespeech.title')"
      ></h3>
      <v-progress-circular
        :size="50"
        indeterminate
        color="primary"
        v-if="loading_plot ? 'primary' : false"
        class="my-10"
      ></v-progress-circular>
      <div id="tweet_hatespeech_mentions_all"></div>
    </v-card>
    <br />

    <br />
    <v-card class="ma-2" elevation="10">
      <h3
        class="text-center pa-4"
        v-html="$t('elections.hatespeech.title_minorities')"
      ></h3>
      <v-progress-circular
        :size="50"
        indeterminate
        color="primary"
        v-if="loading_plot ? 'primary' : false"
        class="my-10"
      ></v-progress-circular>
      <div id="tweet_hatespeech_minorities_all"></div>
    </v-card>
    <br />

    <h2 class="text-center pa-4">{{ $t("elections.individual.title") }}</h2>
    <v-expansion-panels class="my-10" popout multiple>
      <v-expansion-panel
        class="elevation-10"
        v-for="(candidate, i) in candidateNames"
        :key="i"
        @click="displayCandidate(candidate, i)"
      >
        <v-expansion-panel-header>
          <v-avatar size="48" max-width="48px" class="elevation-2">
            <img
              :src="
                candidates[candidate._id].metrics[0].pic.replace(
                  '_normal',
                  '_bigger'
                )
              "
              alt="imagem de perfil"
            />
          </v-avatar>
          &nbsp; &nbsp;
          {{ candidate.name }}
          <v-spacer></v-spacer>

          <v-btn
            :href="`https://twitter.com/${
              candidates[candidate._id].metrics[0].screen_name
            }`"
            icon
            color="primary"
            rounded
            max-width="150px"
          >
            <v-icon>mdi-twitter</v-icon>&nbsp; perfil
          </v-btn>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="text-left">
          <v-row>
            <v-col class="col-sm-2 col-md-3 col-lg-4">
              <v-img
                :src="
                  candidates[candidate._id].metrics[0].pic.replace(
                    '_normal',
                    '_200x200'
                  )
                "
                :lazy-src="candidates[candidate._id].metrics[0].pic"
                aspect-ratio="1"
                max-height="200"
                max-width="200"
                class="mx-auto"
              />
            </v-col>
            <v-col
              class="col-sm-10 col-md-9 col-lg-8"
              align-self="center"
              v-html="
                $t('elections.individual.description', {
                  candidate: candidate.name,
                  followers: candidates[
                    candidate._id
                  ].metrics[0].followers_count.toLocaleString(),
                  days: x.length,
                  tweets: sum(
                    candidates[candidate._id].metrics.map(
                      (m) => m.tweets.length
                    )
                  ),
                  original: sum(
                    candidates[candidate._id].metrics.map(
                      (x) => x.tweets.filter((t) => t.type == 'original').length
                    )
                  ).toLocaleString(),
                  retweets: sum(
                    candidates[candidate._id].metrics.map(
                      (x) => x.tweets.filter((t) => t.type == 'retweet').length
                    )
                  ).toLocaleString(),
                  replies: sum(
                    candidates[candidate._id].metrics.map(
                      (x) => x.tweets.filter((t) => t.type == 'reply').length
                    )
                  ).toLocaleString(),
                  quotes: sum(
                    candidates[candidate._id].metrics.map(
                      (x) => x.tweets.filter((t) => t.type == 'quote').length
                    )
                  ).toLocaleString(),
                  impact: sum(
                    candidates[candidate._id].metrics.map((m) =>
                      sum(
                        m.tweets.map(
                          (t) =>
                            t.favorite_count +
                            (t.type == 'retweet' ? 0 : t.retweet_count)
                        )
                      )
                    )
                  ).toLocaleString(),
                  impact_daily: (
                    sum(
                      candidates[candidate._id].metrics.map((m) =>
                        sum(
                          m.tweets.map(
                            (t) =>
                              t.favorite_count +
                              (t.type == 'retweet' ? 0 : t.retweet_count)
                          )
                        )
                      )
                    ) / x.length
                  )
                    .toFixed(1)
                    .toLocaleString(),
                })
              "
            >
            </v-col>
          </v-row>
          <!-- {{ candidates[candidate.name] }} -->

          <!-- <div :id="`performance_over_time_${candidate._id}`"></div> -->

          <h3 class="mb-0 pb-0 mx-auto" style="display: table">
            {{ $t("elections.individual.plots.mentions") + candidate.name }}
          </h3>
          <div :id="`mentions_over_time_${candidate._id}`"></div>

          <h3 class="mb-0 pb-0 mx-auto" style="display: table">
            {{ $t("elections.individual.plots.impact") + candidate.name }}
          </h3>
          <div :id="`tweet_impact_over_time_${candidate._id}`"></div>

          <h3 class="mb-0 pb-0 mx-auto" style="display: table">
            {{ $t("elections.individual.plots.followers") + candidate.name }}
          </h3>
          <div :id="`followers_over_time_${candidate._id}`"></div>

          <v-data-table
            :headers="tableHeaders()"
            sort-by="favorite_count"
            :sort-desc="false"
            :items="
              candidates[candidate._id].metrics
                .map((x) =>
                  x.tweets.map((t) => {
                    let d = new Date(t.created_at);
                    //t.created_at = d.toLocaleDateString('pt-PT');
                    let year = d.getUTCFullYear();
                    let month = (d.getUTCMonth() + 1)
                      .toString()
                      .padStart(2, '0');
                    let day = d.getUTCDate().toString().padStart(2, '0');
                    t.created_at = `${year}/${month}/${day}`;
                    return t;
                  })
                )
                .flat()
            "
            item-key="_id"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title
                  >{{ candidate.name }} ({{
                    candidates[candidate._id].metrics
                      .map((x) => x.tweets)
                      .flat().length
                  }}
                  tweets)</v-toolbar-title
                >
                <v-spacer></v-spacer>
                <!-- <v-text-field
                  v-model="candidates[candidate._id].search"
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
    this.fetchHateSpeech();
    // read relevant data
    this.x = r.data.history[0].map((d) => new Date(d));
    // this.totals = r.data.history[1].map((x) => x.total).reverse();
    this.candidates = {};
    r.data.history[1].forEach((list, i) => {
      // this.candidates[candidate]
      let _ids = Object.keys(list.candidates);
      _ids.forEach((_id) => {
        let name = list.candidates[_id].name;
        if (this.candidates[_id] === undefined)
          this.candidates[_id] = { _id, name, metrics: [], search: "" };
        this.candidates[_id].metrics.push(list.candidates[_id]);
      });
    });
    // transform object into sorted array
    // this.candidates = Object.values(this.candidates);

    this.candidateNames = Object.values(this.candidates).map((c) => {
      return { name: c.name, _id: c._id };
    }); // retrieves the last screen_name only
    this.candidateNames.sort((c1, c2) => c1.name.localeCompare(c2.name));

    this.display();
    this.loading_plot = false;
  },
  data: function () {
    return {
      x: [],
      totals: [],
      loading_plot: false,
      candidateNames: [],
      hatespeech: {},
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
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },
    max(arr) {
      return arr.reduce((a, b) => Math.max(a, b));
    },
    async fetchHateSpeech() {
      const r = await this.$axios.get(`task_data`, {
        params: { task_name: "measure hatespeech" },
      });
      this.hatespeech.x = r.data.history[0].map((d) => new Date(d));
      this.hatespeech.candidates = {};
      r.data.history[1].forEach((list, i) => {
        let _ids = Object.keys(list.candidates);
        _ids.forEach((_id) => {
          if (this.hatespeech.candidates[_id] === undefined) {
            this.hatespeech.candidates[_id] = {
              _id,
              metrics: [],
            };
          }
          let daily_metrics = list.candidates[_id];
          daily_metrics.total_hits = daily_metrics.hits.length;
          daily_metrics.hits_percent =
            daily_metrics.total_replies > 0
              ? daily_metrics.total_hits / daily_metrics.total_replies
              : 0;
          daily_metrics.minority_arr = daily_metrics.hits
            .map((hit) => hit.minority)
            .filter((minority) => minority !== false);
          daily_metrics.minority_map = daily_metrics.minority_arr.reduce(
            (acc, e) => acc.set(e, (acc.get(e) || 0) + 1),
            new Map()
          );

          this.hatespeech.candidates[_id].metrics.push(list.candidates[_id]);
        });
        _ids.forEach((_id) => {
          let metrics = this.hatespeech.candidates[_id].metrics;
          let minorities = metrics.map((m) => m.minority_arr).flat();
          let minorities_hits = {};
          let minorities_hits_percent = {};
          let minorities_totals = {};
          let minorities_totals_percent = {};
          minorities.forEach((min) => {
            minorities_hits[min] = metrics.map(
              (m) => m.minority_map.get(min) ?? 0
            );
            minorities_hits_percent[min] = metrics.map((m) =>
              m.hits.length > 0 && m.minority_map.has(min)
                ? m.minority_map.get(min) / m.hits.length
                : 0
            );
            minorities_totals[min] = this.sum(
              metrics.map((m) => m.minority_map.get(min) ?? 0)
            );
            minorities_totals_percent[min] = this.sum(
              metrics.map((m) =>
                m.hits.length > 0 && m.minority_map.has(min)
                  ? m.minority_map.get(min) / m.hits.length
                  : 0
              )
            );
          });
          let daily_hits = metrics.map((m) => m.total_hits);
          let hits_percent = metrics.map((m) => m.hits_percent);
          this.hatespeech.candidates[_id].stats = {
            daily_hits,
            hits_percent,
            minorities_hits,
            minorities_hits_percent,
            minorities_totals,
            minorities_totals_percent,
          };
        });
      });
      this.displayHateSpeech();
      this.displayMinoritiesRadar();
    },
    displayHateSpeech() {
      let tracesHate = this.candidateNames.map((cand, i) => {
        let c = this.hatespeech.candidates[cand._id];
        return {
          x: this.x,
          y: c.stats.daily_hits,
          type: "scatter",
          mode: "lines+markers",
          name: `${cand.name}`,
        };
      });
      Plotly.newPlot(`tweet_hatespeech_mentions_all`, tracesHate, {
        colorway: this.colorway,
      });
    },
    displayMinoritiesRadar() {
      let minorities = Object.entries(this.hatespeech.candidates)
        .map((entry) => Object.keys(entry[1].stats.minorities_hits))
        .flat()
        .filter((v, i, a) => a.indexOf(v) === i); //unique minority keys
      let all_minority_values = [];
      let data = this.candidateNames.map((cand, i) => {
        let percent = this.hatespeech.candidates[cand._id].stats
          .minorities_totals_percent;
        all_minority_values.push(minorities.map((min) => percent[min] ?? 0));
        return {
          type: "scatterpolar",
          r: minorities.map((min) => percent[min] ?? 0),
          theta: minorities,
          fill: "toself",
          name: cand.name,
          closedTrace: true,
        };
      });

      let layout = {
        polar: {
          radialaxis: {
            visible: true,
            range: [0, this.max(all_minority_values.flat())],
          },
        },
        autosize: true,
        height: 600,
      };

      Plotly.newPlot("tweet_hatespeech_minorities_all", data, layout);
    },
    tableHeaders() {
      return [
        {
          text: this.$i18n.tc("elections.individual.tweets_table._id"),
          value: "_id",
          align: "center",
        },
        {
          text: this.$i18n.t("elections.individual.tweets_table.type"),
          value: "type",
          align: "center",
        },
        {
          text: this.$i18n.t("elections.individual.tweets_table.full_text"),
          value: "full_text",
          align: "center",
        },
        {
          text: this.$i18n.t(
            "elections.individual.tweets_table.favorite_count"
          ),
          value: "favorite_count",
          align: "center",
        },
        {
          text: this.$i18n.t("elections.individual.tweets_table.retweet_count"),
          value: "retweet_count",
          align: "center",
        },
        {
          text: this.$i18n.t("elections.individual.tweets_table.created_at"),
          value: "created_at",
          align: "center",
        },
        // { text: "", value: "data-table-expand" },
      ];
    },
    calculate_deltas(arr) {
      let res = [0];
      for (let i = 0; i < arr.length - 1; i++) res.push(arr[i] - arr[i + 1]);
      return res;
    },
    display() {
      let tracesMentions = this.candidateNames.map((cand, i) => {
        let c = this.candidates[cand._id];
        return {
          x: this.x,
          y: c.metrics.map((m) => m.name_mentions + m.mentions),
          type: "scatter",
          mode: "lines+markers",
          name: `${cand.name.replace(/[0-9]/g, "").trim()}`,
        };
      });
      Plotly.newPlot(`mentions_over_time_all`, tracesMentions, {
        colorway: this.colorway,
        // title: `Menções ao longo do tempo`,
      });
      let tracesImpact = this.candidateNames.map((cand, i) => {
        let c = this.candidates[cand._id];
        let tweet_impact = c.metrics.map((m) =>
          this.sum(
            m.tweets.map(
              (t) =>
                t.favorite_count + (t.type == "retweet" ? 0 : t.retweet_count)
            )
          )
        );
        return {
          x: this.x,
          y: tweet_impact, //c.metrics.map((m) => m.tweet_impact), // bad historically
          type: "scatter",
          mode: "lines+markers",
          name: `${cand.name}`,
        };
      });
      Plotly.newPlot(`tweet_impact_over_time_all`, tracesImpact, {
        colorway: this.colorway,
        // title: `Impacto ao longo do tempo (likes+retweets)`,
      });

      let tracesFollowers = this.candidateNames.map((cand, i) => {
        let c = this.candidates[cand._id];
        return {
          x: this.x,
          y: this.calculate_deltas(c.metrics.map((m) => m.followers_count)),
          type: "scatter",
          mode: "lines+markers",
          name: `Δ ${cand.name}`,
        };
      });
      Plotly.newPlot(`followers_over_time_all`, tracesFollowers, {
        colorway: this.colorway,
        // title: `Novos seguidores diários`,
      });
    },
    displayCandidate(cand, i) {
      setTimeout(() => {
        let c = this.candidates[cand._id];
        let followers_count = this.calculate_deltas(
          c.metrics.map((x) => x.followers_count)
        );
        let name_mentions = c.metrics.map((x) => x.name_mentions);
        let mentions = c.metrics.map((x) => x.mentions);
        //  let tweet_impact = c.metrics.map((x) => x.tweet_impact);
        let tweet_impact = c.metrics.map((m) =>
          this.sum(
            m.tweets.map(
              (t) =>
                t.favorite_count + (t.type == "retweet" ? 0 : t.retweet_count)
            )
          )
        );
        let tweet_count = c.metrics.map((x) => x.tweets.length);
        let tweet_count_original = c.metrics.map(
          (x) => x.tweets.filter((t) => t.type == "original").length
        );
        let options = {
          colorway: ["EF7B45", "4F6D7A", "16DB65", "947BD3", "0CAADC"],
        };
        Plotly.newPlot(
          `mentions_over_time_${c._id}`,
          [
            {
              x: this.x,
              y: name_mentions,
              type: "scatter",
              mode: "lines+markers",
              name: `'${c.name.replace(/[0-9]/g, "").trim()}'`,
            },
            {
              x: this.x,
              y: mentions,
              type: "scatter",
              mode: "lines+markers",
              name: `'@${c.metrics[0].screen_name}'`,
            },
          ],
          {
            ...options,
            // , title: `Menções ao longo do tempo para ${c.name}`
          }
        );
        Plotly.newPlot(
          `tweet_impact_over_time_${c._id}`,
          [
            {
              x: this.x,
              y: tweet_impact,
              type: "scatter",
              mode: "lines+markers",
              name: this.$i18n.t("elections.individual.plots.impact_label"),
            },
            {
              x: this.x,
              y: tweet_count,
              type: "scatter",
              mode: "lines+markers",
              name: this.$i18n.t("elections.individual.plots.total_tweets"),
              yaxis: "y2",
            },
            {
              x: this.x,
              y: tweet_count_original,
              type: "scatter",
              mode: "lines+markers",
              name: this.$i18n.t("elections.individual.plots.original_tweets"),
              yaxis: "y2",
            },
          ],
          {
            ...options,
            yaxis: {
              title: this.$i18n.t("elections.individual.plots.daily_impact"),
            },
            yaxis2: {
              title: this.$i18n.t("elections.individual.plots.daily_tweets"),
              overlaying: "y",
              side: "right",
            },
            // title: `Tweets e impacto (likes+retweets) para ${c.name}`,
          }
        );
        //   let FIRST_MEASURED_DAY = new Date(2020, 8, 25, 0, 0, 0, 0); // 8 == september
        //   let exclude_left = this.x.filter(
        //     (d) => d.getTime() < FIRST_MEASURED_DAY.getTime()
        //   ).length;
        //   Plotly.newPlot(
        //     `followers_over_time_${c._id}`,
        //     [
        //       {
        //         x: this.x.slice(exclude_left - 1),
        //         y: followers_count.slice(exclude_left - 1),
        //         type: "scatter",
        //         mode: "lines+markers",
        //         name: "seguidores",
        //       },
        //     ],
        //     { ...options, title: `Seguidores ao longo do tempo para ${c.name}` }
        //   );

        Plotly.newPlot(
          `followers_over_time_${c._id}`,
          [
            {
              x: this.x,
              y: followers_count,
              type: "scatter",
              mode: "lines+markers",
              name: "Δ seguidores",
            },
          ],
          {
            ...options,
            // title: `Novos seguidores diários para ${c.name}`,
          }
        );
      }, 200);
    },
  },
  fetchOnServer: false,
};
</script>
