<template>
  <v-container fill-height>
    <v-row no-gutters>
      <v-col cols="12" sm="12" md="6" lg="3">
        <v-card
          class="mx-auto"
          max-width="500"
          :loading="$fetchState.pending ? 'primary' : false"
        >
          <h3 v-if="$fetchState.pending" class="text-center ma-4">
            A carregar...
          </h3>
          <h3 v-if="$fetchState.error" class="red--text text-center">
            Não foi possível carregar os logs
          </h3>
          <span v-else-if="!$fetchState.pending">
            <v-list>
              <v-list-group v-for="(log, task) in logs" :key="task" no-action>
                <template v-slot:activator>
                  <v-list-item-content>
                    <v-list-item-title>
                      <v-tooltip top v-if="log.elapsed">
                        <template v-slot:activator="{ on }">
                          <v-icon v-on="on" color="green" size="small"
                            >mdi-circle</v-icon
                          >
                        </template>
                        <span>
                          a executar há {{ log.elapsed[1] }}
                          <br />
                          começou em {{ log.elapsed[0] }}
                        </span>
                      </v-tooltip>
                      <span>
                        <span class="text--disabled">{{
                          task.split("/")[0]
                        }}</span>
                        /{{ task.split("/")[1] }}
                      </span>
                    </v-list-item-title>
                  </v-list-item-content>
                </template>

                <v-list-item
                  v-for="(file, i) in log.logs"
                  :key="file"
                  @click="loadLogs"
                  :task="task"
                  :index="i"
                  :file="file"
                >
                  <v-list-item-content>
                    <v-list-item-title v-text="file" />
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
            </v-list>
          </span>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="6" lg="9" class="mt-sm-10 mt-md-0">
        <v-card
          v-if="content != '' || selected != null"
          class="ml-6 pa-4 code-height overflow-y-auto"
          :loading="selected.loading ? 'primary' : false"
          max-width="100%"
        >
          <h3 v-if="selected.loading" class="text-center ma-4">
            A carregar...
          </h3>
          <!-- <h3 v-if=".error" class="red--text text-center">Could not load logs</h3> -->
          <div v-else>
            <h3 class="text-center mb-3">
              <span class="text--disabled text-center">{{
                selected.task
              }}</span>
              /
              {{ selected.file }}
            </h3>
            <code class="pa-2" v-html="content.replace('\n', '<br/>')" />
          </div>
        </v-card>
        <v-btn
          v-if="content != ''"
          fixed
          fab
          bottom
          right
          href="#"
          color="primary"
        >
          <v-icon>mdi-arrow-up</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.code-height {
  max-width: 100%;
}
</style>

<script>
export default {
  async fetch() {
    const data = await this.$axios.get(`logs`);
    this.logs = data.data;
  },
  data() {
    return {
      logs: [],
      content: "",
      selected: null,
    };
  },
  methods: {
    loadLogs(e) {
      const t = e.target.closest(".v-list-item");
      this.selected = {
        task: t.getAttribute("task"),
        index: t.getAttribute("index"),
        file: t.getAttribute("file"),
        loading: true,
      };
      this.$axios
        .get(`log`, {
          params: this.selected,
        })
        .then((res) => {
          this.content = res.data.content;
          this.selected.loading = false;
        })
        .catch((_error) => {
          this.content = "Erro de comunicação, por favor tente novamente.";
          this.selected.loading = false;
        });
    },
  },
  fetchOnServer: false,
};
</script>
