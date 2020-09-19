<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant && $vuetify.breakpoint.lgAndUp"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" router exact>
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn v-if="drawer" icon @click.stop="miniVariant = !miniVariant">
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-text-field
        flat
        solo
        hide-details
        prepend-inner-icon="mdi-lan-connect"
        label="endpoint URL"
        v-model="baseURL"
        @keydown.enter="reload"
      />
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  created: function() {
    this.$axios.setBaseURL(
      this.$cookies.get("baseURL") || this.$axios.defaults.baseURL
    );
    this.baseURL = this.$axios.defaults.baseURL;
  },
  data() {
    return {
      baseURL: this.baseURL,
      clipped: true,
      // drawer: this.$vuetify.lgAndUp ? true : false,
      drawer: true,
      fixed: true,
      items: [
        {
          icon: "mdi-apps",
          title: "Welcome",
          to: "/"
        },
        {
          icon: "mdi-chart-line",
          title: "Stats",
          to: "/stats"
        },
        {
          icon: "mdi-text-box-multiple-outline",
          title: "Logs",
          to: "/logs"
        } /* ,
        {
          icon: "mdi-brain",
          title: "Analysis",
          to: "/analysis"
        } */
      ],
      miniVariant: false,
      title: "Twitter Watch"
    };
  },
  methods: {
    reload: function() {
      // this.$axios.setBaseURL(_new);
      this.$cookies.set("baseURL", this.baseURL, {
        path: "/",
        maxAge: 60 * 60 * 24 * 7 * 52 * 100
      });
      window.location.reload(true);
    }
  }
};
</script>
