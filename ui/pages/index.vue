<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <v-card
        class="col-sm-12 col-md-8 col-lg-8 mx-auto my-10"
        style="max-width: 800px"
      >
        <v-card-title style="text-align: center"
          >Bem-vind@ ao Election Watch</v-card-title
        >
        <v-card-text>
          <p class="text-subtitle-1 text-justify" style="font-weight: 500">
            Vivemos tempos atribulados. A tecnologia avança mais rápido do que a
            sociedade consegue assimilar e traz consigo consequências, boas e
            más. As boas são insubstituíveis, mas as más são assustadoras. As
            redes sociais são indiscutivelmente um oceano de informação onde a
            mentira se dissolve na verdade e onde qualquer um pode despejar um
            balde daquilo que acha ser a verdade, ou daquilo que quer que ela
            seja. Este projeto é um pequeno esforço de <i>separar as águas</i>,
            de mostrar e evidenciar que há um perigo para a verdade, para
            justiça, para o planeta, para a democracia e, em última análise,
            para vida de cada um de nós. O objetivo deste projeto é dar uma
            visão mais analítica e transparente sobre a realidade das redes
            sociais em Portugal, com particular relevo para as Eleições
            Presidenciais Portuguesas a ocorrer em janeiro de 2021. <br />O
            Election Watch é um projeto filho do
            <a href="https://github.com/msramalho/twitter-watch/"
              >Twitter Watch</a
            >, uma ferramenta de recolha de dados desenvolvida no âmbito de uma
            <a href="https://msramalho.github.io/msc-thesis.pdf"
              >tese de mestrado</a
            >
            na Faculdade de Engenharia da Universidade do Porto. O código fonte
            é
            <a href="https://github.com/msramalho/election-watch">aberto</a> e
            qualquer cidadão pode
            <a href="https://github.com/msramalho/election-watch/issues"
              >fazer sugestões ou reportar erros</a
            >
            .
          </p>
          <hr />
          De momento, ainda só estamos a monitorizar o Twitter português, mas
          planeamos integrar outras redes sociais em breve.
          <!-- <br />
          <br />
          <v-row no-gutters>
            <v-btn small class="ma-2 col-3" color="primary" nuxt to="/general"
              ><v-icon>mdi-twitter</v-icon>&nbsp;visão geral</v-btn
            >
            <v-btn small class="ma-2 col-3" color="primary" nuxt to="/elections"
              ><v-icon>mdi-twitter</v-icon>&nbsp;presidenciais</v-btn
            >
            <v-btn small class="ma-2 col-3" color="primary" nuxt to="/malicious"
              ><v-icon>mdi-twitter</v-icon>&nbsp;atividade maliciosa</v-btn
            >
          </v-row>
          <br />
          <br />
          <v-btn small nuxt to="/stats">base de dados</v-btn>
          <v-btn small nuxt to="/logs">procesos de recolha</v-btn> -->
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
