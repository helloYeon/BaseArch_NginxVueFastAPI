<template>
  <v-dialog v-model="isActiveComputed" width="20%" @click:outside="cancelEvent">
    <v-card title="表示件数" class="card">
      <v-card-text>
        <v-select
          v-model="size"
          label="表示件数"
          :items="INVOICE_LIST_SIZE_STATUS"
          variant="outlined"
        />
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn class="button" text="キャンセル" @click="cancelEvent"></v-btn>
        <v-btn
          class="button"
          text="保存"
          @click="emit('confirmSize', size ?? INVOICE_LIST_DEFAULT_SIZE)"
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useCookies } from 'vue3-cookies'
import {
  INVOICE_LIST_SIZE,
  INVOICE_LIST_DEFAULT_SIZE,
  INVOICE_LIST_SIZE_STATUS,
} from '@/const/const'

interface DialogProps {
  isActive: boolean
}

interface DialogEmits {
  (e: 'update:isActive', isActive: boolean): void
  (e: 'closeDialog'): void
  (e: 'confirmSize', size: number): void
}

const props = defineProps<DialogProps>()
const emit = defineEmits<DialogEmits>()

const cookies = useCookies()

const isActiveComputed = computed({
  get: () => props.isActive,
  set: (value: boolean) => {
    emit('update:isActive', value)
  },
})

const size = ref(
  Number(cookies.cookies.get(INVOICE_LIST_SIZE) ?? INVOICE_LIST_DEFAULT_SIZE)
)

const cancelEvent = () => {
  size.value = cookies.cookies.get(INVOICE_LIST_SIZE)
    ? Number(cookies.cookies.get(INVOICE_LIST_SIZE))
    : INVOICE_LIST_DEFAULT_SIZE
  emit('closeDialog')
}
</script>

<style lang="scss" scoped>
.card {
  color: #222222;
}

.button {
  font-size: 12px;
  width: 82px;
}
</style>
