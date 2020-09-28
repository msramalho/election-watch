<template>
  <div>
    <v-card class="ma-4 my-10" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">Contas Suspensas</h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Nos últimos {{ x.length - 1 }} dias, foram suspensas um total de
        <strong>{{ this.suspended.length }} contas</strong>. Há várias
        <a
          href="https://help.twitter.com/en/managing-your-account/suspended-twitter-accounts#:~:text=In%20order%20to%20maintain%20a,reasons%20for%20suspension%20may%20include%3A&text=Abusive%20Tweets%20or%20behavior%3A%20We,violating%20our%20Rules%20surrounding%20abuse."
        >
          razões para a suspensão de contas </a
        >. Nem sempre uma suspensão corresponde a comportamento malicioso para a
        comunidade.
      </p>
      <div id="suspensions_over_time"></div>

      <h2 class="text-center pa-4">Lista de contas suspensas</h2>
      <v-data-table
        :headers="tableHeaders"
        :items="suspended"
        item-key="_id"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Contas suspensas</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Pesquisar"
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">More info about {{ item.name }}</td>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "measure suspensions" },
    });

    // read relevant data
    this.x = r.data.history[0].map((d) => new Date(d)).reverse();
    this.totals = r.data.history[1].map((x) => x.total).reverse();
    //ignore zeroes on the left
    let countIgnore = 0;
    for (let i = 1; i < this.totals.length; i++) {
      if (this.totals[i] > 0) {
        countIgnore = i - 1;
        break;
      }
    }
    this.x = this.x.slice(countIgnore);
    this.totals = this.totals.slice(countIgnore);

    // get suspended accounts information
    this.suspended = r.data.history[1]
      .filter((x) => x.users.length > 0)
      .map((x) => x.users)
      .flat()
      .map((user) => {
        // apply any transformation here
        if (user.created_at !== undefined) {
          user.created_at = new Date(user.created_at).toLocaleDateString();
        }
        return user;
      });
    this.suspended = this.uniqBy(this.suspended, (x) => x._id);

    this.display();
  },
  data() {
    return {
      x: [],
      totals: [],
      last_updated: false,
      loading_plot: false,
      dialog_sites: false,
      suspended: [],
      search: "",
      tableHeaders: [
        { text: "ID", value: "_id", align: "center" },
        { text: "Handle", value: "screen_name", align: "center" },
        { text: "Likes", value: "favourites_count", align: "center" },
        { text: "Seguidores", value: "followers_count", align: "center" },
        { text: "Segue", value: "friends_count", align: "center" },
        { text: "Total Tweets", value: "statuses_count", align: "center" },
        { text: "Descrição", value: "description", align: "center" },
        { text: "Criada", value: "created_at", align: "center" },
        // { text: "", value: "data-table-expand" },
      ],
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },
    uniqBy(a, key) {
      var seen = {};
      return a.filter(function (item) {
        var k = key(item);
        return seen.hasOwnProperty(k) ? false : (seen[k] = true);
      });
    },
    display() {
      let startDate = this.x.filter((day, i) => this.totals[i] > 0)[0];
      let options = {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
        // xaxis: {
        //   range: [startDate, this.x[0]],
        //   type: "date",
        // },
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
      Plotly.newPlot("suspensions_over_time", traces, {
        ...options,
        title: "Contas suspensas por dia",
      });

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
