<template>
  <div>
    <h3 class="ma-4">
      Tamanho BD: {{ Math.round(stats.mb) }}MB ({{
        Math.round(stats.mb / 1024, 2)
      }}GB)
    </h3>
    <v-row>
      <v-col cols="12" sm="12" md="6" lg="4">
        <v-card>
          <v-card-title class="subheading font-weight-bold"
            >Tweets</v-card-title
          >
          <v-divider />
          <v-list>
            <v-list-item v-for="(v, k) in stats.tweets" :key="k">
              <v-list-item-content>{{ k }}</v-list-item-content>
              <v-list-item-content class="align-end">{{
                v.toLocaleString()
              }}</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="6" lg="4">
        <v-card>
          <v-card-title class="subheading font-weight-bold">Users</v-card-title>
          <v-divider />
          <v-list>
            <v-list-item v-for="(v, k) in stats.users" :key="k">
              <v-list-item-content>{{ k }}</v-list-item-content>
              <v-list-item-content class="align-end">{{
                v.toLocaleString()
              }}</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  async fetch() {
    console.log();
    const data = await this.$axios.get(`stats`);
    this.stats = data.data;
  },
  data() {
    return {
      stats: Object,
    };
  },
  methods: {},
  fetchOnServer: false,
};
</script>
