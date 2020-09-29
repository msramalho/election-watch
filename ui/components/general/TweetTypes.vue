<template>
  <div>
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">Análise dos diferentes tipos de tweets</h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Os dois gráficos abaixo mostram a evolução diária dos quatro tipos de tweets possíveis:
        <ul>
          <li><i>originals</i> : texto escrito diretamente pelo dono de uma conta</li>
          <li><i>retweets</i> : tweet original partilhado por outro utilizador</li>
          <li><i>quotes</i> : um retweet com novo conteúdo textual adicionado</li>
          <li><i>reply</i> : uma resposta direta a um tweet, aparecendo tipicamente abaixo do mesmo</li>
        </ul>
        <br>
        É importante realçar que o número de contas observadas pode variar e, com elas, o número de tweets diários. Contudo isto pode ser cruzado com os valores na página <nuxt-link to="/stats">Estatísticas BD</nuxt-link>.
        <br/>
      </p>
      <div id="types_of_tweets_totals"></div>
      <br>
      <div id="types_of_tweets_percent"></div>

      <h3 class="text-center pa-4">Algumas estatísticas gerais</h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        <v-simple-table>
          <thead>
            <tr>
              <td>Estatística</td>
              <td>Valor</td>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Total de tweets nos últimos {{x.length}} dias</td><td>{{sum(daily).toLocaleString()}}</td>
            </tr>
            <tr><td>Média diária</td><td>{{parseInt((sum(daily)/daily.length)).toLocaleString()}}</td></tr>
            <tr><td>Máximo diário</td><td>{{max(daily).toLocaleString()}}</td></tr>
            <tr><td>Mínimo diário</td><td>{{min(daily).toLocaleString()}}</td></tr>
          </tbody>
        </v-simple-table>
      </p>
      <br>
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
        title: "Valores normalizados (percentagem)",
      });
      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
