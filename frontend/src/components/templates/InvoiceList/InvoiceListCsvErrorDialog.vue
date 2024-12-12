<template>
  <v-dialog
    v-model="isActiveComputed"
    min-width="30%"
    width="unset"
    @click:outside="emit('closeDialog')"
  >
    <v-card min-height="300px" class="card">
      <v-card-text
        v-if="!csvCheckPeppolIds.length"
        class="d-flex justify-center align-center"
      >
        <v-icon icon="mdi-alert-outline" size="60" />
        <p class="font-weight-bold text-h4 ml-8">請求書がありません。</p>
      </v-card-text>
      <v-card-text v-else class="d-flex justify-center align-start mt-8">
        <v-icon icon="mdi-alert-outline" size="60" />
        <div class="ml-8">
          <p class="peppol-id__title font-weight-bold mb-4">
            下記のPeppolIDに「支払先コード」が設定されていないため、ダウンロードできません。<br />
            ご確認ください。
          </p>
          <p v-for="peppolId in csvCheckPeppolIds" :key="peppolId">
            {{ peppolId }}
          </p>
        </div>
      </v-card-text>
      <CommonErrorDialogButton @dialog-button="emit('closeDialog')" />
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import CommonErrorDialogButton from '../Common/CommonErrorDialogButton.vue'

interface DialogProps {
  isActive: boolean
  csvCheckPeppolIds: string[]
}

interface DialogEmits {
  (e: 'update:isActive', isActive: boolean): void
  (e: 'closeDialog'): void
}

const props = defineProps<DialogProps>()
const emit = defineEmits<DialogEmits>()

const isActiveComputed = computed({
  get: () => props.isActive,
  set: (value: boolean) => {
    emit('update:isActive', value)
  },
})
</script>

<style lang="scss" scoped>
.card {
  color: #222222;
}
.peppol-id {
  &__title {
    font-size: 1.6rem;
  }
}
</style>
