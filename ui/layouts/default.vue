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
        <!-- home -->
        <v-list-item to="/" router exact>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Início</v-list-item-title>
        </v-list-item>
        <!-- nested -->
        <v-list-group
          v-for="item in nestedItems"
          :key="item.title"
          v-model="item.open"
          :prepend-icon="item.action"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </template>
          <v-list-item
            dense
            v-for="child in item.items"
            :key="child.title"
            :to="child.to"
            router
            exact
          >
            <v-list-item-action style="margin-left:10px;">
              <v-icon>{{ child.action }}</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title v-text="child.title"></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{child.tooltip}}</span>
            </v-tooltip>
          </v-list-item>
        </v-list-group>
        <!-- disabled -->
        <v-list-item v-for="item in disabledItems" :key="item.title" disabled>
          <v-list-item-icon>
            <v-icon>{{ item.action }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{item.title}}</v-list-item-title>
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
  created: function () {
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
      nestedItems: [
        {
          action: "mdi-twitter",
          title: "Twitter",
          open: false,
          items: [
            {
              title: "Visão Geral",
              tooltip: "Visão geral sobre a atividade do Twitter em Portugal",
              to: "/general",
              action: "mdi-chart-line",
            },
            {
              title: "Presidenciais 2021",
              tooltip: "Análise da atividade dos candidatos e partidos",
              to: "/elections",
              action: "mdi-vote-outline",
            },
            {
              title: "Atividade Maliciosa",
              tooltip:
                "Explorar a atividade maliciosa: fake news, contas suspensas, atividade de bots",
              to: "/malicious",
              action: "mdi-shield-alert-outline",
            },
            {
              title: "Estatísticas BD",
              tooltip: "Estado atual da Base de Dados",
              to: "/stats",
              action: "mdi-database-check",
            },
            {
              title: "Logs",
              tooltip: "Registos do processo de recolha de dados",
              to: "/logs",
              action: "mdi-text-box-multiple-outline",
            },
          ],
        },
      ],
      disabledItems: [
        {
          action: "mdi-facebook",
          title: "Facebook",
        },
        {
          action: "mdi-youtube",
          title: "Youtube",
        },
        // {
        //   action: "mdi-instagram",
        //   title: "Instagram",
        //   disabled: true,
        // },
      ],
      miniVariant: false,
      title: "Election Watch - presidenciais 2021",
    };
  },
  methods: {
    reload: function () {
      // this.$axios.setBaseURL(_new);
      this.$cookies.set("baseURL", this.baseURL, {
        path: "/",
        maxAge: 60 * 60 * 24 * 7 * 52 * 100,
      });
      window.location.reload(true);
    },
  },
};
</script>
