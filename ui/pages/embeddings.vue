<template>
  <v-layout class="ma-0 pa-0">
    <v-flex class="text-center ma-0 pa-0">
      <!-- <h1 class="my-10">Representação Estrutural em <i>Embeddings</i></h1> -->
      <p class="col-lg-12 mx-auto text-justify">
        Nesta página encontra-se uma representação da proximidade das relações
        entre diferentes contas, mapeada a partir das relações de menções que
        co-ocorrem. É expectável que as contas mais parecidas e, portanto,
        visualmente próximas, partilham do seu contexto. Exemplos de contextos
        de diferentes magnitudes: espaço político, partido político, país,
        cidadãos de uma cidade, fãs de um clube de futebol. Pode abri esta
        visualização numa página dedicada
        <a
          href="https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/msramalho/0ab73d31cd6008486f3e08dd663b3c0b/raw/fe6c91930124a9aed1e67fb2ab7cdf3470ae7c28/config.json"
          >aqui</a
        >.
      </p>
      <iframe
        src="https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/msramalho/0ab73d31cd6008486f3e08dd663b3c0b/raw/fe6c91930124a9aed1e67fb2ab7cdf3470ae7c28/config.json"
        style="width: 100%; height: 800px"
        title="Embeddings visualization"
      >
        <!-- <iframe
        src="https://projector.tensorflow.org/"
        style="width: 100%; height: 800px"
        title="Embeddings visualization"
      > -->
      </iframe>
    </v-flex>
  </v-layout>
</template>