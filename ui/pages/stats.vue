<template>
  <v-layout>
    <v-flex>
      <h1 class="text-center mb-8">Some Statistics</h1>
      <statistics />
      <plot-stats />
    </v-flex>
  </v-layout>
</template>

<script>
import Statistics from "~/components/Statistics.vue";
import PlotStats from "~/components/PlotStats.vue";
export default {
  components: { Statistics, PlotStats }
};
</script>
