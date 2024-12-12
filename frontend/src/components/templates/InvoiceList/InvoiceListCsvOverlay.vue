<template>
  <v-overlay
    :model-value="true"
    location-strategy="connected"
    scroll-strategy="block"
    :persistent="true"
    class="align-center justify-center overlay"
  >
    <p class="overlay__text">{{ text }}</p>
  </v-overlay>
</template>

<script lang="ts" setup>
interface InvoiceListCsvOverlayProps {
  text: string
}

defineProps<InvoiceListCsvOverlayProps>()
</script>

<style lang="scss" scoped>
.overlay {
  &__text {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
    font-size: 5rem;
  }
}
</style>
