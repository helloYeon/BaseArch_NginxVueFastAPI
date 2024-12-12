<template>
  <v-btn
    v-if="!isHiddenCancelButton"
    variant="outlined"
    color="#222222"
    size="large"
    class="button"
    :loading="apiProgressStore.cancelSetting"
    @click="emit('cancelEvent')"
  >
    変更前に戻す
  </v-btn>
  <v-btn
    color="#b11048"
    size="large"
    class="button"
    :loading="apiProgressStore.saveSetting"
    @click="emit('saveEvent')"
  >
    変更を保存
  </v-btn>
</template>

<script setup lang="ts">
import { useApiProgressStore } from '@/store/apiProgress'

interface InvoiceSettingButtonsProps {
  isHiddenCancelButton: boolean
}

interface InvoiceSettingButtonsEmits {
  (e: 'cancelEvent'): void
  (e: 'saveEvent'): void
}

defineProps<InvoiceSettingButtonsProps>()
const emit = defineEmits<InvoiceSettingButtonsEmits>()

const apiProgressStore = useApiProgressStore()
</script>

<style lang="scss" scoped>
.button {
  font-size: 1.4rem;
  & + & {
    margin-left: 16px;
  }
}
</style>
