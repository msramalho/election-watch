<template>
  <v-layout>
    <v-flex class="text-center">
      <h1 class="my-10">{{ $t("elections.title") }}</h1>
      <candidates />
      <polarization />
    </v-flex>
  </v-layout>
</template>

<script>
import Candidates from "~/components/elections/Candidates.vue";
import Polarization from "~/components/elections/Polarization.vue";
export default {
  components: { Candidates, Polarization },
};
</script>