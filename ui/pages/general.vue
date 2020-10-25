<template>
  <v-layout>
    <v-flex class="text-center">
      <h1 class="my-10">{{ $t("general.title") }}</h1>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        {{ $t("general.description") }}
      </p>
      <br />
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