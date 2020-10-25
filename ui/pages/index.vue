<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <v-card
        class="col-sm-12 col-md-8 col-lg-8 mx-auto my-10"
        style="max-width: 800px"
      >
        <v-card-title style="text-align: center">{{
          $t("index.title")
        }}</v-card-title>
        <v-card-text>
          <p
            class="text-subtitle-1 text-justify"
            style="font-weight: 500"
            v-html="$t('index.manifest')"
          ></p>
          <hr />
          {{ $t("index.footer") }}
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  components: {},
};
</script>
