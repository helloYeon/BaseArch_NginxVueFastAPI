<template>
  <v-card-actions class="d-flex justify-center mb-8">
    <v-btn
      variant="outlined"
      class="button font-weight-bold"
      @click="emit('dialogButton')"
    >
      {{ text }}
    </v-btn>
  </v-card-actions>
</template>

<script lang="ts" setup>
interface CommonErrorDialogButtonProps {
  text?: string
}
interface CommonErrorDialogButtonEmits {
  (e: 'dialogButton'): void
}

withDefaults(defineProps<CommonErrorDialogButtonProps>(), {
  text: 'OK',
})
const emit = defineEmits<CommonErrorDialogButtonEmits>()
</script>

<style lang="scss" scoped>
.button {
  min-width: 180px;
  padding: 0 16px;
  font-size: 1.5rem;
}
</style>
