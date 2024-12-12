<template>
  <v-container>
    <PageTitle title="企業統合設定" />
    <v-row class="setting-company-infos">
      <v-col>
        <SettingCompanyInfosTable
          v-model:company-infos="companyInfosComputed"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { GetCompanyInfos200ResponsePayloadInner } from '@/codegen'
import PageTitle from '@/components/parts/PageTitle.vue'
import SettingCompanyInfosTable from './SettingCompanyInfosTable.vue'

interface SettingCompanyInfosProps {
  companyInfos: GetCompanyInfos200ResponsePayloadInner[]
}

interface SettingCompanyInfosEmits {
  (
    e: 'update:companyInfos',
    companyInfos: GetCompanyInfos200ResponsePayloadInner[]
  ): void
}

const props = defineProps<SettingCompanyInfosProps>()
const emit = defineEmits<SettingCompanyInfosEmits>()

const companyInfosComputed = computed({
  get: () => props.companyInfos,
  set: (value) => emit('update:companyInfos', value),
})
</script>

<style lang="scss" scoped>
.setting-company-infos {
  margin: 32px 0 0;
}
</style>
