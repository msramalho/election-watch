<template>
  <div>
<<<<<<< HEAD
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <p class="pa-5">
=======
    <br />
    <v-card class="ma-2" :loading="loading_plot ? 'primary' : false">
      <h3 class="text-center pa-4">Contas por ano e mês de criação</h3>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
>>>>>>> d3af856ea436c53198b51f678bf6a636a50c5d17
        A data de criação das contas é um dos principais fatores que levantam
        suspeitas sobre intenção de atividade maliciosa. O pico na criação de
        contas registado entre março e abril de 2020 mostra-se como uma
        consequência direta do confinamento imposto pela pandemia Covid-19. Este
        fenómeno foi também descrito na
        <a href="https://msramalho.github.io/msc-thesis.pdf"
          >tese de mestrado</a
        >
        que suporta a criação desta ferramenta.
      </p>
<<<<<<< HEAD
      <h2 class="text-center pa-4">Contas por ano e mês de criação</h2>
=======
>>>>>>> d3af856ea436c53198b51f678bf6a636a50c5d17
      <div id="users_by_creation_date"></div>
    </v-card>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  async fetch() {
    this.loading_plot = true;
    const r = await this.$axios.get(`task_data`, {
      params: { task_name: "measure creation dates" },
    });

    this.date = r.data.history[0][0]; //only contains this date
    this.data_points = r.data.history[1][0].filter(
      (dp) => dp.year !== null && dp.year != 1970
    );
    this.x = this.data_points.map((dp) => new Date(dp.year, dp.month - 1, 1));
    this.y = this.data_points.map((dp) => dp.count);

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
      let traces = [
        {
          x: this.x,
          y: this.y,
          stackgroup: "one",
          name: "#contas",
        },
      ];
      Plotly.newPlot("users_by_creation_date", traces, {
        colorway: ["16DB65", "947BD3", "0CAADC", "EF7B45", "4F6D7A"],
      });

      this.loading_plot = false;
    },
  },
  fetchOnServer: false,
};
</script>
