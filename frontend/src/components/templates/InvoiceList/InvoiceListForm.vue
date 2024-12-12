<template>
  <h2 class="mt-4 py-2 search-title">検索条件</h2>
  <v-form v-model="isValid">
    <v-row dense>
      <v-col cols="3">
        <label class="label">フリーワード</label>
        <v-text-field
          v-model.trim="freeWord"
          clearable
          variant="outlined"
          density="compact"
          :error-messages="freeWordValidate.errorMessage.value"
        />
      </v-col>
      <v-col>
        <label class="label">請求書タイプ</label>
        <v-select
          v-model="selectedDataType"
          clearable
          :items="INVOICE_DATA_TYPE_STATUS"
          variant="outlined"
          density="compact"
          placeholder="請求書タイプ"
        />
      </v-col>
      <v-col>
        <label class="label">請求書番号</label>
        <v-text-field
          v-model.trim="invNo"
          clearable
          variant="outlined"
          density="compact"
          :error-messages="invNoValidate.errorMessage.value"
        />
      </v-col>
      <v-col>
        <label class="label">取引先名</label>
        <v-text-field
          v-model.trim="companyName"
          clearable
          variant="outlined"
          density="compact"
          :error-messages="companyNameValidate.errorMessage.value"
        />
      </v-col>
      <v-col cols="3">
        <label class="label">発行日</label>
        <div class="d-flex">
          <div class="w-100">
            <InputDate
              v-model:input-date="fromIssueDate"
              placeholder="開始日"
            />
          </div>
          <p class="mx-1 mt-2">～</p>
          <div class="w-100">
            <InputDate
              v-model:input-date="toIssueDate"
              placeholder="終了日"
              :error-messages="toIssueDateValidate.errorMessage.value"
            />
          </div>
        </div>
      </v-col>
      <v-col>
        <label class="label">支払期日</label>
        <InputDate v-model:input-date="payDueDate" placeholder="期日" />
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="3">
        <label class="label">請求金額</label>
        <div class="d-flex">
          <div class="w-100">
            <v-text-field
              v-model="fromInvAmount"
              placeholder="請求金額"
              clearable
              variant="outlined"
              density="compact"
              :error-messages="fromInvAmountValidate.errorMessage.value"
            />
          </div>
          <p class="mx-1 mt-2">～</p>
          <div class="w-100">
            <v-text-field
              v-model="toInvAmount"
              placeholder="請求金額"
              clearable
              variant="outlined"
              density="compact"
              :error-messages="toInvAmountValidate.errorMessage.value"
            />
          </div>
        </div>
      </v-col>
      <v-col>
        <label class="label">支払方法</label>
        <v-select
          v-model="selectedPaymentMethod"
          clearable
          :items="INVOICE_PaymentMethod_STATUS"
          variant="outlined"
          density="compact"
          placeholder="未選択"
        />
      </v-col>
      <v-col cols="1">
        <label class="label">開封</label>
        <v-select
          v-model="selectedIsOpen"
          :items="INVOICE_OPEN_STATUS"
          clearable
          variant="outlined"
          density="compact"
          placeholder="未選択"
        />
      </v-col>
      <v-col cols="1">
        <label class="label">確認</label>
        <v-select
          v-model="selectedIsConfirmation"
          clearable
          :items="INVOICE_CONFIRMATION_STATUS"
          variant="outlined"
          density="compact"
          placeholder="未選択"
        />
      </v-col>
      <v-col>
        <label class="label">ダウンロード</label>
        <v-select
          v-model="selectedIsDownload"
          clearable
          :items="INVOICE_DOWNLOAD_STATUS"
          variant="outlined"
          density="compact"
          placeholder="未選択"
        />
      </v-col>
      <v-col cols="3">
        <label class="label">受信日時</label>
        <div class="d-flex">
          <div class="w-100">
            <InputDatetime
              v-model:input-datetime="fromReceiveDateTime"
              placeholder="受信日時"
            />
          </div>
          <p class="mx-1 mt-2">～</p>
          <div class="w-100">
            <InputDatetime
              v-model:input-datetime="toReceiveDateTime"
              placeholder="受信日時"
              :error-messages="toReceiveDateTimeValidate.errorMessage.value"
            />
          </div>
        </div>
      </v-col>
      <v-col align-self="center" cols="1">
        <v-btn
          block
          color="#b11048"
          height="35px"
          :loading="apiProgressStore.invoicesSearch"
          :disabled="isDisabledComputed"
          class="button"
          @click="emit('formEmit')"
        >
          検索
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import {
  INVOICE_DATA_TYPE_STATUS,
  INVOICE_PaymentMethod_STATUS,
  INVOICE_OPEN_STATUS,
  INVOICE_CONFIRMATION_STATUS,
  INVOICE_DOWNLOAD_STATUS,
  INVOICE_LIST_VALIDATION_MESSAGES,
} from '@/const/const'
import InputDate from '@/components/parts/InputDate.vue'
import InputDatetime from '@/components/parts/InputDatetime.vue'
import { useGetInvoicesRequestStore } from '@/store/getInvoicesRequest'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import { formatDate } from '@/plugins/utils'
import { useApiProgressStore } from '@/store/apiProgress'
import { VoidTypeAnnotation } from '@babel/types'

interface InvoiceListFormEmits {
  (e: 'formEmit'): VoidTypeAnnotation
}

const emit = defineEmits<InvoiceListFormEmits>()

const requestStore = useGetInvoicesRequestStore()
const apiProgressStore = useApiProgressStore()

const freeWord = computed({
  get: () => requestStore.freeWord,
  set: (value) => {
    requestStore.freeWord = value ? value : undefined
  },
})
const invNo = computed({
  get: () => requestStore.invNo,
  set: (value) => {
    requestStore.invNo = value ? value : undefined
  },
})
const selectedDataType = computed({
  get: () => requestStore.dataType,
  set: (value) => {
    requestStore.dataType = value ?? undefined
  },
})
const companyName = computed({
  get: () => requestStore.companyName,
  set: (value) => {
    requestStore.companyName = value ? value : undefined
  },
})
const fromIssueDate = computed({
  get: () =>
    requestStore.fromIssueDate
      ? new Date(requestStore.fromIssueDate)
      : undefined,
  set: (value) => {
    requestStore.fromIssueDate = value
      ? formatDate(value, 'yyyy-MM-dd')
      : undefined
  },
})
const toIssueDate = computed({
  get: () =>
    requestStore.toIssueDate ? new Date(requestStore.toIssueDate) : undefined,
  set: (value) => {
    requestStore.toIssueDate = value
      ? formatDate(value, 'yyyy-MM-dd')
      : undefined
  },
})
const payDueDate = computed({
  get: () =>
    requestStore.payDueDate ? new Date(requestStore.payDueDate) : undefined,
  set: (value) => {
    requestStore.payDueDate = value
      ? formatDate(value, 'yyyy-MM-dd')
      : undefined
  },
})
const fromInvAmount = computed({
  get: () => requestStore.fromInvAmount,
  set: (value) => {
    requestStore.fromInvAmount = value ? value : undefined
  },
})
const toInvAmount = computed({
  get: () => requestStore.toInvAmount,
  set: (value) => {
    requestStore.toInvAmount = value ? value : undefined
  },
})
const selectedPaymentMethod = computed({
  get: () => requestStore.paymentMethod,
  set: (value) => {
    requestStore.paymentMethod = value ?? undefined
  },
})
const selectedIsOpen = computed({
  get: () => requestStore.isOpen,
  set: (value) => {
    requestStore.isOpen = value ?? undefined
  },
})
const selectedIsConfirmation = computed({
  get: () => requestStore.isConfirmation,
  set: (value) => {
    requestStore.isConfirmation = value ?? undefined
  },
})
const selectedIsDownload = computed({
  get: () => requestStore.isDownload,
  set: (value) => {
    requestStore.isDownload = value ?? undefined
  },
})
const fromReceiveDateTime = computed({
  get: () =>
    requestStore.fromReceiveDateTime
      ? new Date(requestStore.fromReceiveDateTime)
      : undefined,
  set: (value) => {
    requestStore.fromReceiveDateTime = value
      ? formatDate(value, 'yyyy-MM-dd HH:mm')
      : undefined
  },
})
const toReceiveDateTime = computed({
  get: () =>
    requestStore.toReceiveDateTime
      ? new Date(requestStore.toReceiveDateTime)
      : undefined,
  set: (value) => {
    requestStore.toReceiveDateTime = value
      ? formatDate(value, 'yyyy-MM-dd HH:mm')
      : undefined
  },
})

// ボタン非活性処理
const isDisabledComputed = computed(() => {
  if (apiProgressStore.invoicesSearch) return false
  return !isValid.value || apiProgressStore.invoices
})

// バリデーション通過フラグ
const isValid = ref(false)

// useFieldで指定したフィールドの名前でバリデーションスキーマ設定
const validationSchema = yup.object().shape({
  freeWord: yup
    .string()
    .nullable()
    .max(255, INVOICE_LIST_VALIDATION_MESSAGES.MAX_LENGTH),
  invNo: yup
    .string()
    .nullable()
    .max(255, INVOICE_LIST_VALIDATION_MESSAGES.MAX_LENGTH),
  companyName: yup
    .string()
    .nullable()
    .max(255, INVOICE_LIST_VALIDATION_MESSAGES.MAX_LENGTH),
  toIssueDate: yup
    .string()
    .nullable()
    .test(
      'toIssueDateValidate',
      INVOICE_LIST_VALIDATION_MESSAGES.TO_ISSUE_DATE,
      () => {
        if (!fromIssueDate.value || !toIssueDate.value) return true
        const fromDate = new Date(fromIssueDate.value)
        const toDate = new Date(toIssueDate.value)
        return toDate.getTime() >= fromDate.getTime()
      }
    ),
  fromInvAmount: yup
    .number()
    .nullable()
    .min(0, INVOICE_LIST_VALIDATION_MESSAGES.MIN_NUMBER)
    .typeError(INVOICE_LIST_VALIDATION_MESSAGES.NUMBER_TYPE)
    .transform((value, originalValue) =>
      String(originalValue).trim() === '' ? null : value
    ),
  toInvAmount: yup
    .number()
    .nullable()
    .min(0, INVOICE_LIST_VALIDATION_MESSAGES.MIN_NUMBER)
    .typeError(INVOICE_LIST_VALIDATION_MESSAGES.NUMBER_TYPE)
    .transform((value, originalValue) =>
      String(originalValue).trim() === '' ? null : value
    )
    .test(
      'toInvAmountValidate',
      INVOICE_LIST_VALIDATION_MESSAGES.TO_INV_AMOUNT,
      () => {
        if (!fromInvAmount.value || !toInvAmount.value) return true
        return toInvAmount.value >= fromInvAmount.value
      }
    ),
  toReceiveDateTime: yup
    .string()
    .nullable()
    .test(
      'toReceiveDateTimeValidate',
      INVOICE_LIST_VALIDATION_MESSAGES.TO_RECEIVE_DATE_TIME,
      () => {
        if (!fromReceiveDateTime.value || !toReceiveDateTime.value) return true
        const fromDatetime = new Date(fromReceiveDateTime.value)
        const toDatetime = new Date(toReceiveDateTime.value)
        return toDatetime.getTime() >= fromDatetime.getTime()
      }
    ),
})

useForm({
  validationSchema: validationSchema, // ルール設定
  validateOnMount: true, // フォームがマウントされたときにバリデーションを実行する
  initialValues: {
    freeWord: requestStore.freeWord,
    invNo: requestStore.invNo,
    companyName: requestStore.companyName,
    fromIssueDate: requestStore.fromIssueDate,
    toIssueDate: requestStore.toIssueDate,
    fromInvAmount: requestStore.fromInvAmount,
    toInvAmount: requestStore.toInvAmount,
    fromReceiveDateTime: requestStore.fromReceiveDateTime,
    toReceiveDateTime: requestStore.toReceiveDateTime,
  },
})

// バリデーション監視対象の要素定義
// この値を変更することによって、
// バリデーションスキーマで設定した各フィールド名('freeWord', 'invNo' ...etc)のルールでバリデーション実行
const freeWordValidate = useField('freeWord')
const invNoValidate = useField('invNo')
const companyNameValidate = useField('companyName')
const fromIssueDateValidate = useField('fromIssueDate')
const toIssueDateValidate = useField('toIssueDate')
const fromInvAmountValidate = useField('fromInvAmount')
const toInvAmountValidate = useField('toInvAmount')
const fromReceiveDateTimeValidate = useField('fromReceiveDateTime')
const toReceiveDateTimeValidate = useField('toReceiveDateTime')

// 各項目が変更されたときバリデーション監視対象の要素にも値を代入
watch(freeWord, (newValue) => {
  freeWordValidate.value.value = newValue
})
watch(invNo, (newValue) => {
  invNoValidate.value.value = newValue
})
watch(companyName, (newValue) => {
  companyNameValidate.value.value = newValue
})
watch(fromIssueDate, (newValue) => {
  fromIssueDateValidate.value.value = newValue
})
watch(toIssueDate, (newValue) => {
  toIssueDateValidate.value.value = newValue
})
watch(fromInvAmount, (newValue) => {
  fromInvAmountValidate.value.value = newValue
})
watch(toInvAmount, (newValue) => {
  toInvAmountValidate.value.value = newValue
})
watch(fromReceiveDateTime, (newValue) => {
  fromReceiveDateTimeValidate.value.value = newValue
})
watch(toReceiveDateTime, (newValue) => {
  toReceiveDateTimeValidate.value.value = newValue
})
</script>

<style lang="scss">
.search-title {
  font-size: 1.4rem;
  color: #222222;
}

.label {
  color: #222222;
  font-size: 1.2rem;
}

.button {
  font-size: 1.2rem;
}
</style>
