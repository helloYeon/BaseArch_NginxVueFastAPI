<template>
  <v-menu v-model="activeMenu">
    <template #activator="{ props: on }">
      <v-btn
        variant="outlined"
        height="45px"
        min-width="45px"
        rounded="circle"
        v-bind="on"
      >
        <v-icon icon="mdi-dots-vertical" :color="iconColor" size="15" />
      </v-btn>
    </template>

    <v-card width="240px">
      <v-list class="list">
        <v-list-item class="list__item-border" @click="emit('csvDownload')">
          <v-list-item-title class="list__title">
            CSVダウンロード
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          class="list__item-border"
          :disabled="apiProgressStore.invoices"
          @click="emit('openDialog')"
        >
          <v-list-item-title class="list__title"> 表示件数 </v-list-item-title>
        </v-list-item>
        <v-list-item
          :disabled="apiProgressStore.receive"
          @click="emit('invoiceReceives')"
        >
          <v-list-item-title class="list__title">
            {{ invoiceReceivesTitle }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script lang="ts" setup>
import { useApiProgressStore } from '@/store/apiProgress'
import { ref, computed } from 'vue'

interface InvoiceListMenuEmits {
  (e: 'csvDownload'): void
  (e: 'openDialog'): void
  (e: 'invoiceReceives'): void
}

const emit = defineEmits<InvoiceListMenuEmits>()

const apiProgressStore = useApiProgressStore()

const activeMenu = ref(false)
const iconColor = computed(() => {
  return activeMenu.value ? '#b11048' : '#000000'
})

const invoiceReceivesTitle = computed(() => {
  if (apiProgressStore.receive) return '請求書取得中'
  return '請求書の取得'
})
</script>

<style lang="scss" scoped>
.list {
  color: #222222;
  padding: 0;

  &__item-border {
    border-bottom: 1px solid #e8e8e8;
  }

  &__title {
    font-size: 1.4rem;
    text-align: center;
  }
}
</style>
