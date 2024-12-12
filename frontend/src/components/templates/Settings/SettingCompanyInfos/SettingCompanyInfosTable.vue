<template>
  <v-table class="table">
    <thead class="table__header">
      <th>id(company_infos)</th>
      <th>esCompanyId</th>
      <th>会社名</th>
      <th>統合先</th>
    </thead>
    <tbody>
      <tr v-for="companyInfo in companyInfosComputed" :key="companyInfo.id">
        <td>{{ companyInfo.id }}</td>
        <td>{{ companyInfo.esCompanyId }}</td>
        <td>{{ companyInfo.name }}</td>
        <td>
          <v-select
            v-model="companyInfo.parentEsCompanyId"
            :items="companyItems"
            placeholder="-"
            variant="outlined"
            density="compact"
            hide-details
          />
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script lang="ts" setup>
import { GetCompanyInfos200ResponsePayloadInner } from '@/codegen'
import { computed } from 'vue'

interface SettingCompanyInfosTableProps {
  companyInfos: GetCompanyInfos200ResponsePayloadInner[]
}

interface SettingCompanyInfosTableEmits {
  (
    e: 'update:companyInfos',
    companyInfos: GetCompanyInfos200ResponsePayloadInner[]
  ): void
}

const props = defineProps<SettingCompanyInfosTableProps>()
const emit = defineEmits<SettingCompanyInfosTableEmits>()

const companyInfosComputed = computed({
  get: () => props.companyInfos,
  set: (value) => emit('update:companyInfos', value),
})

const companyItems = computed(() => {
  return [
    { title: '-', value: null },
    ...props.companyInfos.map((companyInfo) => {
      return {
        title: companyInfo.name,
        value: companyInfo.esCompanyId,
      }
    }),
  ]
})
</script>

<style lang="scss" scoped>
.table {
  font-size: 12px;
  color: #222222;
  border-bottom: 1px solid #e0e0e0;
  white-space: nowrap;

  &,
  th,
  td {
    border-collapse: collapse;
    border: 1px solid #e0e0e0;
    white-space: nowrap;
  }

  & th {
    padding-left: 16px;
  }

  & td {
    border-bottom: 1px solid #e0e0e0;
  }

  &__header {
    text-align: left;
    background-color: #f6f6f6;
    height: 50px;
  }
}
</style>
