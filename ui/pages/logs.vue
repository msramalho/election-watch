<template>
  <v-layout>
    <v-flex>
      <h1 class="text-center ma-2">Logs de Recolha de Dados</h1>
      <logs-list />
    </v-flex>
  </v-layout>
</template>

<script>
import LogsList from "~/components/LogsList.vue";
export default {
  components: { LogsList },
};
</script>
