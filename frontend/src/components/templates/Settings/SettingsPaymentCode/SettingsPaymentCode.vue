<template>
  <v-container>
    <PageTitle title="支払先コード設定" />
    <v-row
      v-if="companyIntegrations.length > 1 && selectedCompanyInfosIdComputed"
      class="mt-8"
    >
      <v-col cols="5">
        <v-select
          v-model="selectedCompanyInfosIdComputed"
          :items="companyIntegrations"
          :disabled="apiProgressStore.cancelSetting"
          item-title="name"
          item-value="companyInfosId"
          variant="outlined"
          density="compact"
          hide-details
          @update:model-value="changeCompany"
        />
      </v-col>
    </v-row>

    <v-row class="setting-paymentCode">
      <v-col>
        <SettingsPaymentCodeList
          v-model:selected-peppol-ids="selectedPeppolIds"
          :payment-code-list="paymentCodeListComputed"
          @sort="emit('paymentCodeListSort')"
        />
      </v-col>

      <v-col align-self="center" cols="auto">
        <CommonControlButtons @add="addItem" @delete="deleteItem" />
      </v-col>

      <v-col>
        <SettingsPaymentCodeForm
          v-model:peppol-id="inputPeppolId"
          v-model:payment-code="inputPaymentCode"
          :peppol-id-error-message="peppolIdErrorMessage"
          :payment-code-error-message="paymentCodeErrorMessage"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { CompanyIntegrationsItem, PaymentCodeData } from '@/codegen'
import { useApiProgressStore } from '@/store/apiProgress'
import {
  PEPPOL_ID_ERROR_MESSAGE,
  PEPPOL_ID_ERROR_MESSAGE_DUPL,
  PAYMENT_CODE_ERROR_MESSAGE,
  PEPPOL_ID_PATTERN,
  PAYMENT_CODE_PATTERN,
} from '@/const/const'
import PageTitle from '@/components/parts/PageTitle.vue'
import CommonControlButtons from '@/components/templates/Common/CommonControlButtons.vue'
import SettingsPaymentCodeList from '@/components/templates/Settings/SettingsPaymentCode/SettingsPaymentCodeList.vue'
import SettingsPaymentCodeForm from '@/components/templates/Settings/SettingsPaymentCode/SettingsPaymentCodeForm.vue'

interface SettingsAuthProps {
  paymentCodeList: PaymentCodeData[]
  companyIntegrations: CompanyIntegrationsItem[]
  selectedCompanyInfosId: number
}

interface SettingsAuthEmits {
  (e: 'update:paymentCodeList', paymentCodeList: PaymentCodeData[]): void
  (e: 'update:selectedCompanyInfosId', selectedCompanyInfosId: number): void
  (e: 'changeCompany'): void
  (e: 'paymentCodeListSort'): void
}

const props = defineProps<SettingsAuthProps>()

const emit = defineEmits<SettingsAuthEmits>()

const apiProgressStore = useApiProgressStore()

const inputPeppolId = ref('')
const peppolIdErrorMessage = ref('')
const inputPaymentCode = ref('')
const paymentCodeErrorMessage = ref('')
const selectedPeppolIds = ref<string[]>([])

const paymentCodeListComputed = computed({
  get: () => props.paymentCodeList,
  set: (value) => emit('update:paymentCodeList', value),
})

// 選択している企業ID
const selectedCompanyInfosIdComputed = computed({
  get: () => props.selectedCompanyInfosId,
  set: (value) => emit('update:selectedCompanyInfosId', value),
})

// 支払先コード追加
const addItem = () => {
  // バリデーションメッセージ削除
  peppolIdErrorMessage.value = ''
  paymentCodeErrorMessage.value = ''

  // Peppol IDバリデーション
  if (!PEPPOL_ID_PATTERN.test(inputPeppolId.value)) {
    // フォーマットエラー
    peppolIdErrorMessage.value = PEPPOL_ID_ERROR_MESSAGE
  } else if (
    paymentCodeListComputed.value.some(
      ({ peppolId }) => peppolId === inputPeppolId.value.replace(/t/g, 'T')
    )
  ) {
    // 重複
    peppolIdErrorMessage.value = PEPPOL_ID_ERROR_MESSAGE_DUPL
  }

  // 支払先コードバリデーション
  if (!PAYMENT_CODE_PATTERN.test(inputPaymentCode.value)) {
    paymentCodeErrorMessage.value = PAYMENT_CODE_ERROR_MESSAGE
  }

  if (peppolIdErrorMessage.value || paymentCodeErrorMessage.value) return

  paymentCodeListComputed.value.unshift({
    peppolId: inputPeppolId.value.replace(/t/g, 'T'),
    paymentCode: inputPaymentCode.value,
  })

  inputPeppolId.value = ''
  inputPaymentCode.value = ''
}

// 支払先コード削除
const deleteItem = () => {
  if (!selectedPeppolIds.value) return

  const firstDeletedItem = paymentCodeListComputed.value.find(({ peppolId }) =>
    selectedPeppolIds.value.includes(peppolId)
  )

  paymentCodeListComputed.value = paymentCodeListComputed.value.filter(
    ({ peppolId }) => !selectedPeppolIds.value.includes(peppolId)
  )

  inputPeppolId.value = firstDeletedItem?.peppolId ?? ''
  inputPaymentCode.value = firstDeletedItem?.paymentCode ?? ''
}

// 企業変更
const changeCompany = () => {
  emit('changeCompany')
}

watch(inputPeppolId, () => {
  peppolIdErrorMessage.value = ''
})
watch(inputPaymentCode, () => {
  paymentCodeErrorMessage.value = ''
})
</script>

<style lang="scss" scoped>
.setting-paymentCode {
  background-color: #cccccc;
  margin: 32px 0 0;
}
</style>
