<template>
  <v-layout>
    <v-flex class="text-center">
      <h1>Visão Geral</h1>
      <p class="ma-5">
        Nesta página encontra-se uma descrição geral das contas e respetivos
        tweets que estamos a monitorizar, no contexto do Twitter Português.
      </p>
      <tweet-types />
      <creation-dates />
    </v-flex>
  </v-layout>
</template>

<script>
import TweetTypes from "~/components/general/TweetTypes.vue";
import CreationDates from "~/components/general/CreationDates.vue";
export default {
  components: { TweetTypes, CreationDates },
};
</script>