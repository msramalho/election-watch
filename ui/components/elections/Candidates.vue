<template>
  <div>
    <!-- <v-card class="ma-4 my-10" :loading="loading_plot ? 'primary' : false"> -->
    <v-card class="ma-2" elevation="10">
      <h3 class="text-center pa-4">
        Análise das menções por <strong>nome</strong> e por
        <code>@handle</code> para os diferentes candidatos
      </h3>
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
      <h3 class="text-center pa-4">
        Análise do impacto direto da atividade de cada candidato<br />medida
        como a soma do número de <i>likes</i> e <i>retweets</i> aos seus
        <i>tweets</i>
      </h3>
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
        Evolução temporal da variação diária do número de seguidores de cada
        candidato.
      </h3>
      <small>(o período sem alterações corresponde a falta de dados)</small>
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

    <h2 class="text-center pa-4">Análise individual de cada candidato</h2>
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
            <v-col class="col-sm-10 col-md-9 col-lg-8" align-self="center">
              Neste momento, {{ candidate._name }} tem
              <strong>{{
                candidates[
                  candidate._id
                ].metrics[0].followers_count.toLocaleString()
              }}</strong>
              seguidores.
              <br />
              Nos últimos {{ x.length }} dias, publicou
              <strong>
                {{
                  sum(
                    candidates[candidate._id].metrics.map(
                      (m) => m.tweets.length
                    )
                  )
                }}
                tweets
              </strong>
              ({{
                sum(
                  candidates[candidate._id].metrics.map(
                    (x) => x.tweets.filter((t) => t.type == "original").length
                  )
                ).toLocaleString()
              }}
              originais,
              {{
                sum(
                  candidates[candidate._id].metrics.map(
                    (x) => x.tweets.filter((t) => t.type == "retweet").length
                  )
                ).toLocaleString()
              }}
              retweets,
              {{
                sum(
                  candidates[candidate._id].metrics.map(
                    (x) => x.tweets.filter((t) => t.type == "reply").length
                  )
                ).toLocaleString()
              }}
              replies,
              {{
                sum(
                  candidates[candidate._id].metrics.map(
                    (x) => x.tweets.filter((t) => t.type == "quote").length
                  )
                ).toLocaleString()
              }}
              quotes).
              <br />
              Criando um impacto total (likes+retweets) de
              {{
                sum(
                  candidates[candidate._id].metrics.map((m) =>
                    sum(
                      m.tweets.map(
                        (t) =>
                          t.favorite_count +
                          (t.type == "retweet" ? 0 : t.retweet_count)
                      )
                    )
                  )
                ).toLocaleString()
              }}
              ({{
                (
                  sum(
                    candidates[candidate._id].metrics.map((m) =>
                      sum(
                        m.tweets.map(
                          (t) =>
                            t.favorite_count +
                            (t.type == "retweet" ? 0 : t.retweet_count)
                        )
                      )
                    )
                  ) / x.length
                )
                  .toFixed(1)
                  .toLocaleString()
              }}
              por dia).
            </v-col>
          </v-row>
          <!-- {{ candidates[candidate.name] }} -->

          <!-- <div :id="`performance_over_time_${candidate._id}`"></div> -->
          <div :id="`mentions_over_time_${candidate._id}`"></div>
          <div :id="`tweet_impact_over_time_${candidate._id}`"></div>
          <div :id="`followers_over_time_${candidate._id}`"></div>

          <v-data-table
            :headers="tableHeaders"
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
                  >Tweets de {{ candidate.name }} ({{
                    candidates[candidate._id].metrics
                      .map((x) => x.tweets)
                      .flat().length
                  }})</v-toolbar-title
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
        { text: "Data", value: "created_at", align: "center" },
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
    calculate_deltas(arr) {
      let res = [0];
      for (let i = 0; i < arr.length - 1; i++) res.push(arr[i] - arr[i + 1]);
      return res;
    },
    display() {
      let colorway = [
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
      ];
      let tracesMentions = this.candidateNames.map((cand, i) => {
        let c = this.candidates[cand._id];
        return {
          x: this.x,
          y: c.metrics.map((m) => m.name_mentions + m.mentions),
          type: "scatter",
          mode: "lines+markers",
          name: `${cand.name.replace(/[0-9]/g, "")} menções`,
        };
      });
      Plotly.newPlot(`mentions_over_time_all`, tracesMentions, {
        colorway: colorway,
        title: `Menções ao longo do tempo`,
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
          name: `${cand.name} impacto`,
        };
      });
      Plotly.newPlot(`tweet_impact_over_time_all`, tracesImpact, {
        colorway: colorway,
        title: `Impacto ao longo do tempo (likes+retweets)`,
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
        colorway: colorway,
        title: `Variação de seguidores ao longo do tempo`,
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
              name: `menções '${c.name.replace(/[0-9]/g, "")}'`,
            },
            {
              x: this.x,
              y: mentions,
              type: "scatter",
              mode: "lines+markers",
              name: `menções '@${c.metrics[0].screen_name}'`,
            },
          ],
          { ...options, title: `Menções ao longo do tempo para ${c.name}` }
        );
        Plotly.newPlot(
          `tweet_impact_over_time_${c._id}`,
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
            title: `Tweets e impacto (likes+retweets) para ${c.name}`,
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
            title: `Variação de seguidores ao longo do tempo para ${c.name}`,
          }
        );
      }, 200);
    },
  },
  fetchOnServer: false,
};
</script>
