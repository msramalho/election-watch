<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <v-card>
        <v-card-title class="headline">Welcome to the Twitter Watch</v-card-title>
        <v-card-text></v-card-text>
        <v-card-actions>
          <v-btn color="primary" nuxt to="/stats">See stats</v-btn>
          <v-spacer />
          <v-btn color="primary" nuxt to="/logs">See logs</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  components: {}
};
</script>
