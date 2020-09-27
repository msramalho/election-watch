<template>
  <v-layout>
    <v-flex class="text-center">
      <h1>Presidenciais 2021</h1>
      <candidates />
    </v-flex>
  </v-layout>
</template>

<script>
import Candidates from "~/components/elections/Candidates.vue";
export default {
  components: { Candidates },
};
</script>