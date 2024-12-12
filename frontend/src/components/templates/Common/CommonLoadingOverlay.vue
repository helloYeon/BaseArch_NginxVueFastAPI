<template>
  <v-overlay
    :model-value="true"
    location-strategy="connected"
    scroll-strategy="block"
    :persistent="true"
    class="align-center justify-center overlay"
  >
    <v-progress-circular color="primary" size="64" indeterminate />
  </v-overlay>
</template>
