<template>
  <v-row class="header" justify="space-between">
    <v-col class="pr-0">
      <v-row>
        <div class="d-flex justify-start">
          <v-sheet class="header__is-confirmation mr-4">
            <v-select
              v-model="selectedIsConfirmation"
              class="header__is-confirmation__button"
              :items="INVOICE_CONFIRMATION_STATUS"
              :disabled="apiProgressStore.confirm"
              variant="outlined"
              density="compact"
              @update:model-value="
                emit('changeConfirmEmit', selectedIsConfirmation)
              "
            />
          </v-sheet>
          <v-chip
            label
            size="large"
            :prepend-icon="downloadIconComputed"
            color="#B11048"
            class="header__is-download"
          >
            {{ downloadTitleComputed }}
          </v-chip>
        </div>
      </v-row>
      <v-row>
        <h2 class="header__title h-100 pa-1">
          {{ invoice.invoiceTitle }}
        </h2>
      </v-row>
      <v-row>
        <h3 class="header__company-name">
          {{ invoice.publisher?.publisherCompanyNameOrg }}
        </h3>
      </v-row>
      <v-row>
        <v-col class="pt-0 pl-0">
          <p>{{ isSourceTitle }}ID：{{ invoice.publisher?.bizRegistNo }}</p>
          <p>{{ isSourceTitle }}住所：{{ publisherAddressComputed }}</p>
          <p>{{ isSourceTitle }}TEL：{{ invoice.publisher?.publisherPhone }}</p>
          <p>
            {{ isSourceTitle }}アドレス：{{ invoice.publisher?.publisherMail }}
          </p>
        </v-col>
      </v-row>
    </v-col>

    <v-col class="pl-0" lg="5">
      <v-row>
        <v-col class="text-end pr-0 pt-0">
          <span class="mr-4"> 請求書番号：{{ invoice.invNo }} </span>
          <span>請求日：{{ formatDate(invoice.listInfo?.sendDate) }}</span>
        </v-col>
      </v-row>
      <v-row>
        <div class="d-flex align-center w-100 header__total">
          <p class="header__title header__total__amount-title">
            合計金額<span class="header__total__tax">（税込）</span>
          </p>
          <p
            v-if="invoice.invAmount"
            class="header__title text-right w-75 pr-lg-4 font-weight-black"
          >
            {{
              currencyMark(invoice.currencyCode) +
              numToStrNum(invoice.invAmount)
            }}
          </p>
        </div>
      </v-row>
      <v-row>
        <v-col class="pl-0 mt-3">
          <p>支払期限　　　：{{ formatDate(invoice.payDueDate) }}</p>
          <p>支払方法　　　：{{ paymentMethodTitle(invoice.paymentMethod) }}</p>
          <div class="d-flex">
            <p class="header__bank-info-title">支払先口座情報：</p>
            <div>
              <div v-for="item in invoice.banks" :key="item.fnclInstCode">
                <p class="header__bank-code">
                  {{
                    `${item.fnclInstCode ? item.fnclInstCode + ':' : ''}` +
                    `${item.branchCode ? item.branchCode + ':' : ''}` +
                    `${item.depositSec ? item.depositSec + ':' : ''}` +
                    `${item.accountNum ? item.accountNum : ''}`
                  }}
                </p>
                <p>{{ item.depositorKana }}</p>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { DataType, Invoice, IsConfirmation, IsDownload } from '@/codegen'
import { INVOICE_CONFIRMATION_STATUS } from '@/const/const'
import {
  formatDate,
  numToStrNum,
  paymentMethodTitle,
  currencyMark,
} from '@/plugins/utils'
import { useApiProgressStore } from '@/store/apiProgress'

interface InvoiceDetailHeaderProps {
  invoice: Invoice
}
interface InvoiceDetailHeaderEmit {
  (e: 'changeConfirmEmit', selectedIsConfirmation: IsConfirmation): void
  (e: 'update:confirmation', isConfirmation: IsConfirmation): void
  (e: 'update:download', isDownload: IsDownload): void
}

const emit = defineEmits<InvoiceDetailHeaderEmit>()
const props = defineProps<InvoiceDetailHeaderProps>()

const apiProgressStore = useApiProgressStore()

const selectedIsConfirmation = computed({
  get: () => props.invoice.isConfirmation,
  set: (value) => emit('update:confirmation', value),
})
const isDownloadComputed = computed({
  get: () => props.invoice.isDownload,
  set: (value) => emit('update:download', value),
})

const downloadIconComputed = computed(() => {
  return isDownloadComputed.value === IsDownload.DOWNLOADED
    ? 'mdi-check'
    : 'mdi-download'
})
const downloadTitleComputed = computed(() => {
  return isDownloadComputed.value === IsDownload.DOWNLOADED
    ? 'ダウンロード済み'
    : '未ダウンロード'
})

const isSourceTitle = computed(() => {
  return props.invoice.dataType === DataType.PURCHASESTATEMENT
    ? '請求先'
    : '請求元'
})
const publisherAddressComputed = computed(() => {
  const publisher = props.invoice.publisher
  return `${publisher?.publisherZip ?? ''} ${publisher?.publisherCountrySubentity ?? ''}${publisher?.publisherCityName ?? ''}${publisher?.publisherStreetName ?? ''}`
})
</script>

<style lang="scss" scoped>
h2,
p,
span {
  font-size: 12px;
  color: #222222;
}

.header {
  border: 1px solid #e0e0e0;
  margin: 0;
  padding: 16px;

  &__is-confirmation {
    min-width: 143px;
  }
  &__is-download {
    font-size: 12px;
    height: 35px;
  }

  &__title {
    font-size: 2.4rem;
  }

  &__company-name {
    font-size: 2rem;
    color: #222222;
    margin-top: 12px;
  }

  &__total {
    border: 1px solid #b11048;
    height: 46px;

    &__amount-title {
      background-color: #b11048;
      color: white;
      min-width: 160px;
      text-align: center;
      width: 50%;
      height: 100%;
      padding: 4px;
    }

    &__tax {
      font-size: 1.3rem;
      color: #ffffff;
    }
  }

  &__back-info-title {
    min-width: 98px;
  }

  &__bank-code {
    word-break: break-all;
  }
}
</style>
