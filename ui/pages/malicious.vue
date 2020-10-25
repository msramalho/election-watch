<template>
  <v-layout>
    <v-flex class="text-center">
      <h1 class="my-10">{{ $t("malicious.title") }}</h1>
      <fakenews />
      <suspensions />
    </v-flex>
  </v-layout>
</template>

<script>
import Fakenews from "~/components/malicious/Fakenews.vue";
import Suspensions from "~/components/malicious/Suspensions.vue";
export default {
  components: { Fakenews, Suspensions },
};
</script>