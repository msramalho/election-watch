<template>
  <v-layout class="ma-0 pa-0">
    <v-flex class="text-center ma-0 pa-0">
      <p
        class="col-lg-12 mx-auto text-justify"
        v-html="
          $t('embeddings.description', {
            href:
              'https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/msramalho/0ab73d31cd6008486f3e08dd663b3c0b/raw/455da367ba49d0347e2a99157749b2296eda2ee2/config.json',
          })
        "
      ></p>
      <iframe
        src="https://projector.tensorflow.org/?config=https://gist.githubusercontent.com/msramalho/0ab73d31cd6008486f3e08dd663b3c0b/raw/455da367ba49d0347e2a99157749b2296eda2ee2/config.json"
        style="width: 100%; height: 800px"
        title="3d embeddings"
      >
      </iframe>
    </v-flex>
  </v-layout>
</template>