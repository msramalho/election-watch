<template>
  <v-layout>
    <v-flex class="text-center">
      <h1 class="my-10">Representação Estrutural em <i>Embeddings</i></h1>
      <p class="pa-5 pb-0 col-sm-12 col-md-10 col-lg-8 mx-auto text-justify">
        Nesta página encontra-se uma descrição geral das contas e respetivos
        tweets que estamos a monitorizar, no contexto do Twitter Português.
      </p>
      <br />
      <a href="https://projector.tensorflow.org/">See source</a>
      <!-- <iframe
      src="https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/msramalho/0ab73d31cd6008486f3e08dd663b3c0b/raw/5b1dcfbda42420b13591da5ceec23893e0f6afd8/config.json"
      style="width: 100%; height: 800px"
      title="Embeddings visualization"
    > -->
      <iframe
        src="https://projector.tensorflow.org/"
        style="width: 100%; height: 800px"
        title="Embeddings visualization"
      >
      </iframe>
    </v-flex>
  </v-layout>
</template>