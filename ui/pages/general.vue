<template>
  <v-layout>
    <v-flex class="text-center">
      <h1>Visão Geral</h1>
<<<<<<< HEAD
      <p class="ma-5">
        Nesta página encontra-se uma descrição geral das contas e respetivos
        tweets que estamos a monitorizar, no contexto do Twitter Português.
      </p>
=======
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Nesta página encontra-se uma descrição geral das contas e respetivos
        tweets que estamos a monitorizar, no contexto do Twitter Português.
      </p>
      <br />
>>>>>>> d3af856ea436c53198b51f678bf6a636a50c5d17
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