<template>
  <v-row align="center" justify="space-between">
    <v-col class="search-result-text" cols="auto">
      検索結果：{{ total }}件
    </v-col>
    <v-col v-if="companyIntegrations.length > 1" cols="2">
      <v-select
        v-model="selectedCompanyInfosId"
        class="companies"
        :items="companyIntegrations"
        :disabled="apiProgressStore.invoices"
        item-title="name"
        item-value="companyInfosId"
        variant="outlined"
        density="compact"
        hide-details
        @update:model-value="changeCompany"
      />
    </v-col>
    <v-spacer />
    <v-col cols="auto" class="search-result-text">
      最終受信日時：{{ lastReceiveDateTime }}
    </v-col>
    <v-col cols="auto">
      <v-pagination
        v-model="selectedPage"
        class="pagination"
        :length="pages"
        :total-visible="4"
        :disabled="apiProgressStore.invoices"
        color="#222222"
        size="2.4rem"
        @update:model-value="pagination"
      />
    </v-col>
    <v-col cols="auto">
      <InvoiceListMenu
        @csv-download="emit('csvDownload')"
        @open-dialog="emit('openDialog')"
        @invoice-receives="emit('invoiceReceives')"
      />
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <p v-if="!invoices.length" class="no-item-message">請求書はありません</p>
      <v-table v-if="invoices.length" class="table" hover>
        <thead>
          <tr class="table__header">
            <th class="unopened-icon" />
            <th
              class="id font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.INVOICEID)"
              @click="sort(GetInvoicesSortEnum.INVOICEID)"
            >
              <div class="d-flex align-center">
                ID
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th class="font-weight-black">請求書タイプ</th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.INVNO)"
              @click="sort(GetInvoicesSortEnum.INVNO)"
            >
              <div class="d-flex align-center">
                請求書番号
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.COMPANYNAME)"
              @click="sort(GetInvoicesSortEnum.COMPANYNAME)"
            >
              <div class="d-flex align-center">
                取引先名
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th
              class="table__send-date font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.ISSUEDATE)"
              @click="sort(GetInvoicesSortEnum.ISSUEDATE)"
            >
              <div class="d-flex align-center">
                請求書／通知書発行日
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.PAYDUEDATE)"
              @click="sort(GetInvoicesSortEnum.PAYDUEDATE)"
            >
              <div class="d-flex align-center">
                支払期日
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.INVAMOUNT)"
              @click="sort(GetInvoicesSortEnum.INVAMOUNT)"
            >
              <div class="d-flex justify-end align-center">
                請求金額(税込)
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.PAYMENTMETHOD)"
              @click="sort(GetInvoicesSortEnum.PAYMENTMETHOD)"
            >
              <div class="d-flex align-center">
                支払方法
                <InvoiceListTableSortIcon />
              </div>
            </th>
            <th class="font-weight-black">ステータス</th>
            <th
              class="font-weight-black cursor-pointer"
              :class="sortClass(GetInvoicesSortEnum.RECEIVE_DATE_TIME)"
              @click="sort(GetInvoicesSortEnum.RECEIVE_DATE_TIME)"
            >
              <div class="d-flex align-center">
                受信日時
                <InvoiceListTableSortIcon />
              </div>
            </th>
          </tr>
        </thead>
        <tbody v-for="item in invoices" :key="item.invoiceId">
          <tr class="table__body-row" @click="emit('transitionInfo', item)">
            <td class="unopened-icon">
              <v-icon
                v-if="item.isOpen === IsOpen.UNOPENED"
                icon="mdi-circle"
                size="10px"
                color="#b11048"
                title="未開封"
              />
            </td>
            <td class="id">
              {{ item.invoiceId }}
            </td>
            <td>{{ dataTypeTitle(item.dataType) }}</td>
            <td>{{ item.invNo }}</td>
            <td class="table__company-name">
              {{ item.publisher?.publisherCompanyNameOrg ?? '' }}
            </td>
            <td class="table__send-date">
              {{ formatDate(item.listInfo?.sendDate) }}
            </td>
            <td>{{ formatDate(item.payDueDate) }}</td>
            <td class="text-right">
              <span v-if="item.invAmount !== null">{{
                currencyMark(item.currencyCode)
              }}</span
              >{{ numToStrNum(item.invAmount) }}
            </td>
            <td>
              {{ paymentMethodTitle(item.paymentMethod) }}
            </td>
            <td>
              <div class="d-flex">
                <v-icon
                  class="ml-2 mr-3"
                  :icon="ConfirmIcon"
                  :color="confirmIconColor(item.isConfirmation)"
                  :title="confirmIconTitle(item.isConfirmation)"
                />
                <v-icon
                  :icon="DownloadIcon"
                  :color="downloadIconColor(item.isDownload)"
                  :title="downloadIconTitle(item.isDownload)"
                />
              </div>
            </td>
            <td>
              {{ formatDate(item.receiveDateTime, 'yyyy/MM/dd HH:mm') }}
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import ConfirmIcon from '@/components/parts/ConfirmIcon.vue'
import DownloadIcon from '@/components/parts/DownloadIcon.vue'
import InvoiceListMenu from '@/components/templates/InvoiceList/InvoiceListMenu.vue'
import {
  CompanyIntegrationsItem,
  GetInvoicesSortEnum,
  GetInvoicesSortOrderEnum,
  InvoiceListData,
  IsConfirmation,
  IsDownload,
  IsOpen,
} from '@/codegen'
import {
  dataTypeTitle,
  formatDate,
  numToStrNum,
  paymentMethodTitle,
  currencyMark,
} from '@/plugins/utils'
import { useGetInvoicesRequestStore } from '@/store/getInvoicesRequest'
import { useApiProgressStore } from '@/store/apiProgress'
import InvoiceListTableSortIcon from './InvoiceListTableSortIcon.vue'

interface InvoiceListTableProps {
  pages: number
  total: number
  invoices: InvoiceListData[]
  companyIntegrations: CompanyIntegrationsItem[]
  page: number
  lastReceiveDateTime: string
  companyInfosId: number
}

interface InvoiceListTableEmits {
  (e: 'paginationList', page: number): void
  (e: 'sortList', sort: GetInvoicesSortEnum): void
  (e: 'update:page', page: number): void
  (e: 'update:companyInfosId', companyInfosId: number): void
  (e: 'transitionInfo', invoice: InvoiceListData): void
  (e: 'changeCompany', companyInfosId: number): void
  (e: 'csvDownload'): void
  (e: 'openDialog'): void
  (e: 'invoiceReceives'): void
}

const props = defineProps<InvoiceListTableProps>()
const emit = defineEmits<InvoiceListTableEmits>()

const requestStore = useGetInvoicesRequestStore()
const apiProgressStore = useApiProgressStore()

// 現在の企業
const selectedCompanyInfosId = computed({
  get: () => props.companyInfosId,
  set: (value) => emit('update:companyInfosId', value),
})

// 現在のページ
const selectedPage = computed({
  get: () => props.page,
  set: (value) => emit('update:page', value),
})

// 確認アイコン
const confirmIconColor = computed(() => (isConfirmation: IsConfirmation) => {
  return isConfirmation === IsConfirmation.CONFIRMED ? '#b11048' : '#dbd8d8'
})
const confirmIconTitle = computed(() => (isConfirmation: IsConfirmation) => {
  return isConfirmation === IsConfirmation.CONFIRMED ? '確認済' : '未確認'
})
// ダウンロードアイコン
const downloadIconColor = computed(() => (isDownload: IsDownload) => {
  return isDownload === IsDownload.DOWNLOADED ? '#b11048' : '#dbd8d8'
})
const downloadIconTitle = computed(() => (isDownload: IsDownload) => {
  return isDownload === IsDownload.DOWNLOADED
    ? 'ダウンロード済み'
    : '未ダウンロード'
})

// 企業変更
const changeCompany = (companyInfosId: number) => {
  emit('changeCompany', companyInfosId)
}

// ページネーション
const pagination = (page: number) => {
  emit('paginationList', page)
}

// ソート
const sort = (sort: GetInvoicesSortEnum) => {
  if (apiProgressStore.invoices) return
  emit('sortList', sort)
}
const sortClass = (sort: GetInvoicesSortEnum) => {
  return {
    asc:
      requestStore.sort === sort &&
      requestStore.sortOrder === GetInvoicesSortOrderEnum.ASC,
    desc:
      requestStore.sort === sort &&
      requestStore.sortOrder === GetInvoicesSortOrderEnum.DESC,
  }
}
</script>

<style lang="scss" scoped>
.search-result-text {
  color: #222222;
  font-weight: bold;
  font-size: 12px;
}
.companies {
  max-width: 200px;
  font-size: 12px;
  color: #222222;
}
.pagination {
  font-size: 12px;
}
.no-item-message {
  text-align: center;
  color: #222222;
}
.table {
  font-size: 12px;
  color: #222222;
  border-bottom: 1px solid #e0e0e0;
  white-space: nowrap;

  & td {
    border-bottom: 1px solid #e0e0e0;
  }

  &__header {
    background-color: #f6f6f6;
  }

  &__body-row:hover {
    cursor: pointer;
    background-color: #fff4f4;
  }

  &__checkbox {
    width: 40px;
    z-index: 2;
  }

  & .id {
    padding-left: 8px;
  }

  & .unopened-icon {
    padding: 0;
    width: 18px;
    padding-left: 8px;
  }

  &__company-name {
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    max-width: 150px;
  }

  &__send-date {
    width: 180px;
  }
}
.is-false {
  color: #dbd8d8;
}
</style>
