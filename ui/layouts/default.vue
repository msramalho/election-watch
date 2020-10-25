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
          <v-list-item-title>{{ $t("default.home") }}</v-list-item-title>
        </v-list-item>
        <!-- nested -->
        <v-list-group
          v-model="nestedItems[0].open"
          :prepend-icon="nestedItems[0].action"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Twitter</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item dense key="general" to="/general" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-chart-line</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.general.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{ this.$i18n.t("default.sidebar.general.tooltip") }}</span>
            </v-tooltip>
          </v-list-item>

          <v-list-item dense key="elections" to="/elections" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-vote-outline</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.elections.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{
                this.$i18n.t("default.sidebar.elections.tooltip")
              }}</span>
            </v-tooltip>
          </v-list-item>

          <v-list-item dense key="malicious" to="/malicious" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-shield-alert-outline</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.malicious.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{
                this.$i18n.t("default.sidebar.malicious.tooltip")
              }}</span>
            </v-tooltip>
          </v-list-item>

          <v-list-item dense key="embeddings" to="/embeddings" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-svg</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.embeddings.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{
                this.$i18n.t("default.sidebar.embeddings.tooltip")
              }}</span>
            </v-tooltip>
          </v-list-item>

          <v-list-item dense key="stats" to="/stats" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-database-check</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.stats.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{ this.$i18n.t("default.sidebar.stats.tooltip") }}</span>
            </v-tooltip>
          </v-list-item>

          <v-list-item dense key="logs" to="/logs" router exact>
            <v-list-item-action style="margin-left: 10px">
              <v-icon>mdi-text-box-multiple-outline</v-icon>
            </v-list-item-action>
            <v-tooltip right open-delay="500">
              <template v-slot:activator="{ on }">
                <v-list-item-content v-on="on">
                  <v-list-item-title
                    v-text="$t('default.sidebar.logs.title')"
                  ></v-list-item-title>
                </v-list-item-content>
              </template>
              <span>{{ this.$i18n.t("default.sidebar.logs.tooltip") }}</span>
            </v-tooltip>
          </v-list-item>
        </v-list-group>
        <!-- disabled -->
        <v-list-item v-for="item in disabledItems" :key="item.title" disabled>
          <v-list-item-icon>
            <v-icon>{{ item.action }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="clipped" app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn v-if="drawer" icon @click.stop="miniVariant = !miniVariant">
        <v-icon>mdi-{{ `chevron-${miniVariant ? "right" : "left"}` }}</v-icon>
      </v-btn>
      <v-toolbar-title v-text="this.$t('default.title')" />
      <v-spacer />
      <!-- <v-text-field
        flat
        solo
        hide-details
        prepend-inner-icon="mdi-lan-connect"
        label="endpoint URL"
        v-model="baseURL"
        @keydown.enter="reload"
      /> -->
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            class="mx-2"
            v-on:click="changeLang"
            v-bind="attrs"
            v-on="on"
            >{{ lang == "pt" ? "en" : "pt" }}</v-btn
          >
        </template>
        <span>{{ $t("default.change_lang") }}</span>
      </v-tooltip>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
      <v-spacer></v-spacer>
      <small>
        <a
          :title="this.$t('default.links.source_code.title')"
          href="https://github.com/msramalho/election-watch"
        >
          {{ this.$t("default.links.source_code.text") }}</a
        >
        &nbsp;|&nbsp;
        <a
          :title="this.$t('default.links.msc_thesis.title')"
          href="https://msramalho.github.io/msc-thesis.pdf"
        >
          {{ this.$t("default.links.msc_thesis.text") }}</a
        >
        &nbsp;|&nbsp;
        <a
          :title="this.$t('default.links.author.title')"
          href="https://www.linkedin.com/in/msramalho/"
        >
          {{ this.$t("default.links.author.text") }}</a
        >
      </small>
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
  mounted() {
    this.$i18n.locale = this.lang;
  },
  data() {
    return {
      lang: this.$cookies.get("app-lang") || this.$store.state.locale || "pt",
      baseURL: this.baseURL,
      clipped: true,
      // drawer: this.$vuetify.lgAndUp ? true : false,
      drawer: true,
      fixed: true,
      nestedItems: [
        {
          action: "mdi-twitter",
          title: "Twitter",
          open: [
            "general",
            "elections",
            "malicious",
            "stats",
            "logs",
            "embeddings",
          ].includes(this.$route.name),
          items: [
            {
              title: this.$i18n.t("default.sidebar.general.title"),
              tooltip: this.$i18n.t("default.sidebar.general.tooltip"),
              to: "/general",
              action: "mdi-chart-line",
            },
            {
              title: this.$i18n.t("default.sidebar.elections.title"),
              tooltip: this.$i18n.t("default.sidebar.elections.tooltip"),
              to: "/elections",
              action: "mdi-vote-outline",
            },
            {
              title: this.$i18n.t("default.sidebar.malicious.title"),
              tooltip: this.$i18n.t("default.sidebar.malicious.tooltip"),
              to: "/malicious",
              action: "mdi-shield-alert-outline",
            },
            {
              title: this.$i18n.t("default.sidebar.embeddings.title"),
              tooltip: this.$i18n.t("default.sidebar.embeddings.tooltip"),
              to: "/embeddings",
              action: "mdi-svg",
            },
            {
              title: this.$i18n.t("default.sidebar.stats.title"),
              tooltip: this.$i18n.t("default.sidebar.stats.tooltip"),
              to: "/stats",
              action: "mdi-database-check",
            },
            {
              title: this.$i18n.t("default.sidebar.logs.title"),
              tooltip: this.$i18n.t("default.sidebar.logs.tooltip"),
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
    changeLang() {
      // toggle between portuguese and english
      this.lang = this.lang == "pt" ? "en" : "pt";
      this.$store.commit("SET_LANG", this.lang);
      this.$cookies.set("app-lang", this.lang);
      this.$i18n.locale = this.lang;
    },
  },
};
</script>
