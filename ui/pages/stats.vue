<template>
  <v-layout>
    <v-flex>
      <h1 class="text-center my-10">{{ $t("statistics.title") }}</h1>
      <statistics />
      <plot-stats />
    </v-flex>
  </v-layout>
</template>

<script>
import Statistics from "~/components/Statistics.vue";
import PlotStats from "~/components/PlotStats.vue";
export default {
  components: { Statistics, PlotStats },
};
</script>
