<template>
  <v-container>
    <PageTitle title="CSV出力項目設定" />
    <v-row class="csv-format">
      <v-col cols="5">
        <v-select
          v-model="csvDownloadTypeComputed"
          :items="SETTINGS_CSV_FORMAT_STATUS"
          variant="outlined"
          density="compact"
          hide-details
        />
      </v-col>
    </v-row>
    <v-row
      v-show="csvDownloadTypeComputed === CsvDownloadType.ALLITEMS"
      class="setting-table"
    >
      <v-col cols="6">
        <SettingsCsvTable
          v-if="common.length"
          v-model:setting-list="commonComputed"
          :type="COMMON_TYPE.NAME"
        />
      </v-col>
    </v-row>
    <v-row
      v-show="csvDownloadTypeComputed === CsvDownloadType.ALLITEMS"
      class="setting-table"
    >
      <v-col>
        <SettingsCsvTable
          v-if="invoiceDetail.length"
          v-model:setting-list="invoiceDetailComputed"
          :type="INVOICE_DETAIL_TYPE.NAME"
        />
      </v-col>
      <v-col>
        <SettingsCsvTable
          v-if="particulars.length"
          v-model:setting-list="particularsComputed"
          :type="PARTICULARS_TYPE.NAME"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNestedAccordionStore } from '@/store/nestedAccordion'
import {
  COMMON_TYPE,
  INVOICE_DETAIL_TYPE,
  PARTICULARS_TYPE,
  SETTINGS_CSV_FORMAT_STATUS,
} from '@/const/const'
import { SettingListInterface } from '@/views/Settings.vue'
import PageTitle from '@/components/parts/PageTitle.vue'
import SettingsCsvTable from '@/components/templates/Settings/SettingsCsv/SettingsCsvTable.vue'
import { CsvDownloadType } from '@/codegen'

interface SettingsCsvProps {
  invoiceDetail: SettingListInterface[]
  particulars: SettingListInterface[]
  common: SettingListInterface[]
  csvDownloadType: CsvDownloadType
}

interface SettingsCsvEmits {
  (e: 'update:invoiceDetail', invoiceDetail: SettingListInterface[]): void
  (e: 'update:particulars', particulars: SettingListInterface[]): void
  (e: 'update:common', common: SettingListInterface[]): void
  (e: 'update:csvDownloadType', csvDownloadType: number): void
}

const props = defineProps<SettingsCsvProps>()

const emit = defineEmits<SettingsCsvEmits>()

const nestedAccordionStore = useNestedAccordionStore()

const invoiceDetailComputed = computed({
  get: () => props.invoiceDetail,
  set: (value) => emit('update:invoiceDetail', value),
})

const particularsComputed = computed({
  get: () => props.particulars,
  set: (value) => emit('update:particulars', value),
})

const commonComputed = computed({
  get: () => props.common,
  set: (value) => emit('update:common', value),
})

const csvDownloadTypeComputed = computed({
  get: () => props.csvDownloadType,
  set: (value) => emit('update:csvDownloadType', value),
})

nestedAccordionStore.$reset()
</script>

<style lang="scss" scoped>
.csv-format {
  margin-top: 32px;
}

.setting-table {
  margin-top: 30px;
  color: #222222;
}
</style>
