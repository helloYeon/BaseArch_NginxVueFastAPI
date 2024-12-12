<template>
  <v-card height="300px" class="card">
    <v-card-text class="d-flex justify-center align-center">
      <v-icon icon="mdi-alert-outline" size="60" />
      <p class="font-weight-bold text-h4 ml-8">
        {{ cardText }}
      </p>
    </v-card-text>

    <CommonErrorDialogButton
      :text="buttonText"
      @dialog-button="emit('dialogButton')"
    />
  </v-card>
</template>

<script lang="ts" setup>
import CommonErrorDialogButton from './CommonErrorDialogButton.vue'

interface DialogCardProps {
  cardText: string
  buttonText?: string
}

interface DialogCardEmits {
  (e: 'dialogButton'): void
}

defineProps<DialogCardProps>()
const emit = defineEmits<DialogCardEmits>()
</script>

<style lang="scss" scoped>
.card {
  color: #222222;
}
</style>
