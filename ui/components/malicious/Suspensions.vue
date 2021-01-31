<template>
  <div>
    <v-card class="ma-4 my-10" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">Contas Suspensas</h3>
      <p
        class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify"
        v-html="
          $t('malicious.suspensions.description', {
            days: x.length - 1,
            suspended: this.suspended.length,
          })
        "
      ></p>
      <div id="suspensions_over_time"></div>

      <h2 class="text-center pa-4">
        {{ $t("malicious.suspensions.table.title") }}
      </h2>
      <v-data-table
        :headers="tableHeaders()"
        :items="suspended"
        item-key="_id"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>{{
              $t("malicious.suspensions.table.toolbar_title")
            }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              :label="$t('malicious.suspensions.table.search_label')"
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
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
    // const r = await this.$axios.get(`task_data`, {params: { task_name: "measure suspensions" },});
    const r = await this.$axios.get(`task_data_measure_suspensions.json`);

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
          user.created_at = new Date(user.created_at).toLocaleDateString(
            "pt-PT"
          );
        }
        return user;
      });
    this.suspended = this.uniqueBy(this.suspended, (x) => x._id);

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
    };
  },
  methods: {
    sum(arr) {
      return arr.reduce((a, b) => a + b, 0);
    },
    tableHeaders() {
      return [
        {
          text: this.$i18n.tc("malicious.suspensions.table.headers._id"),
          value: "_id",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.screen_name"
          ),
          value: "screen_name",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.favourites_count"
          ),
          value: "favourites_count",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.followers_count"
          ),
          value: "followers_count",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.friends_count"
          ),
          value: "friends_count",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.statuses_count"
          ),
          value: "statuses_count",
          align: "center",
        },
        {
          text: this.$i18n.tc(
            "malicious.suspensions.table.headers.description"
          ),
          value: "description",
          align: "center",
        },
        {
          text: this.$i18n.tc("malicious.suspensions.table.headers.created_at"),
          value: "created_at",
          align: "center",
        },
      ];
    },
    uniqueBy(a, key) {
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
