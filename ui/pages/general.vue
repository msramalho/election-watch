<template>
  <v-layout>
    <v-flex class="text-center">
      <h1>Visão Geral</h1>
      <tweet-types />
    </v-flex>
  </v-layout>
</template>

<script>
import TweetTypes from "~/components/general/TweetTypes.vue";
export default {
  components: { TweetTypes },
};
</script>