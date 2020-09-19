<template>
  <v-layout>
    <v-flex>
      <h1 class="text-center ma-2">Data Collection Logs</h1>
      <logs-list />
    </v-flex>
  </v-layout>
</template>

<script>
import LogsList from "~/components/LogsList.vue";
export default {
  components: { LogsList }
};
</script>
