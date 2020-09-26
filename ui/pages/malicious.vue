<template>
  <v-layout>
    <v-flex class="text-center">
      <h1>Atividade Maliciosa</h1>
      <fakenews />
    </v-flex>
  </v-layout>
</template>

<script>
import Fakenews from "~/components/general/Fakenews.vue";
export default {
  components: { Fakenews },
};
</script>