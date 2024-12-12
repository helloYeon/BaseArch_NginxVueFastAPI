<template>
  <v-container>
    <PageTitle title="請求書一覧" class="pb-2" />
    <InvoiceListForm @form-emit="formEmit" />
    <InvoiceListTable
      v-model:page="invoiceListPage"
      v-model:company-infos-id="invoiceListCompanyInfosId"
      :pages="pages"
      :total="total"
      :invoices="invoices"
      :last-receive-date-time="lastReceiveDateTime"
      :company-integrations="companyIntegrations"
      @pagination-list="paginationList"
      @csv-download="csvDownload"
      @open-dialog="openSizeDialog"
      @invoice-receives="postReceive"
      @sort-list="sortList"
      @transition-info="transitionInfo"
      @change-company="changeCompany"
    />
  </v-container>

  <InvoiceListSizeDialog
    v-model:is-active="isSizeDialogActive"
    @close-dialog="closeSizeDialog"
    @confirm-size="confirmSize"
  />
  <InvoiceListCsvErrorDialog
    v-model:is-active="isCsvErrorActive"
    :csv-check-peppol-ids="csvCheckPeppolIds"
    @close-dialog="closeCsvErrorDialog"
  />
  <CommonErrorDialog
    :is-active="is400ErrorActive"
    @close-dialog="close400ErrorDialog"
  />
  <CommonFooter />

  <InvoiceListCsvOverlay
    v-if="apiProgressStore.csv"
    text="ダウンロード中・・・"
  />
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  AuthErrorCode,
  COLLECTION_FORMATS,
  CompanyIntegrationsItem,
  DownloadApi,
  GetInvoicesSortEnum,
  GetInvoicesSortOrderEnum,
  InfoApi,
  IntegrationApi,
  InvoiceListData,
  IsParentCompany,
  ReceiveApi,
  ResponseContext,
  querystring,
} from '@/codegen'
import { ClientConfig } from '@/plugins/apiClient'
import { useCookies } from 'vue3-cookies'
import { useGetInvoicesRequestStore } from '@/store/getInvoicesRequest'
import PageTitle from '@/components/parts/PageTitle.vue'
import InvoiceListForm from '@/components/templates/InvoiceList/InvoiceListForm.vue'
import InvoiceListTable from '@/components/templates/InvoiceList/InvoiceListTable.vue'
import InvoiceListSizeDialog from '@/components/templates/InvoiceList/InvoiceListSizeDialog.vue'
import InvoiceListCsvErrorDialog from '@/components/templates/InvoiceList/InvoiceListCsvErrorDialog.vue'
import InvoiceListCsvOverlay from '@/components/templates/InvoiceList/InvoiceListCsvOverlay.vue'
import CommonFooter from '@/components/templates/Common/CommonFooter.vue'
import CommonErrorDialog from '@/components/templates/Common/CommonErrorDialog.vue'
import { useErrorDialogStore } from '@/store/errorDialog'
import { INVOICE_LIST_SIZE, ROUTE_NAMES } from '@/const/const'
import {
  createDownloadFile,
  getCurrentDateTime,
  getDistanceToNow,
  openErrorDialog,
  setUserInfo,
  transitionLogin,
} from '@/plugins/utils'
import { useApiProgressStore } from '@/store/apiProgress'
import { useOpenStore } from '@/store/open'
import { useLoadingStore } from '@/store/loading'

const router = useRouter()
const cookies = useCookies()

const errorDialogStore = useErrorDialogStore()
const requestStore = useGetInvoicesRequestStore()
const apiProgressStore = useApiProgressStore()
const openStore = useOpenStore()
const loadingStore = useLoadingStore()

const infoApi = new InfoApi(new ClientConfig())

const downloadApi = new DownloadApi(
  new ClientConfig({
    // queryParamsStringifyを上書き
    queryParamsStringify(params) {
      if (typeof params?.['invoice_ids'] === 'string')
        // カンマ区切りの文字列を配列に戻す
        params['invoice_ids'] = params['invoice_ids'].split(
          COLLECTION_FORMATS.csv
        )
      return querystring(params)
    },
  })
)

const receiveApi = new ReceiveApi(
  new ClientConfig({
    // middlewareを上書き
    middleware: [
      {
        post: async (context: ResponseContext) => {
          if (context.response.ok) {
            // ユーザー情報セット
            await setUserInfo()

            return Promise.resolve(context.response)
          }

          const status = context.response.status
          apiProgressStore.$reset()
          // 401 error
          if (status === 401) {
            const { header } = await context.response.json()

            switch (header.code) {
              case AuthErrorCode.E9011:
                router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
                break
              case AuthErrorCode.E9012:
                router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
                break
              case AuthErrorCode.E9013:
                openErrorDialog(header.code)
                break
              case AuthErrorCode.E9014:
                openErrorDialog(header.code)
                break
              case AuthErrorCode.E9015:
                openErrorDialog(header.code)
                break
              case AuthErrorCode.E9016:
                transitionLogin()
                break
              default:
                router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
                break
            }
          }
          // 500 Error
          else if (status >= 500) {
            errorDialogStore.receiveApi500Error = true
            openErrorDialog()
          } else {
            openErrorDialog()
          }
        },
      },
    ],
  })
)

const integrationApi = new IntegrationApi(new ClientConfig())

const pages = ref(1)
const total = ref(0)
const invoices = ref<InvoiceListData[]>([])
const companyIntegrations = ref<CompanyIntegrationsItem[]>([])
const lastReceiveDateTime = ref('')
const isCsvErrorActive = ref(false)
const csvCheckPeppolIds = ref<string[]>([])
const isSizeDialogActive = ref(false)

const is400ErrorActive = computed({
  get: () => errorDialogStore.getErrorDialog,
  set: (value) => errorDialogStore.setErrorDialog(value),
})

const invoiceListPage = computed({
  get: () => requestStore.page,
  set: (value) => {
    requestStore.page = value
  },
})

const invoiceListSort = computed({
  get: () => requestStore.sort,
  set: (value) => (requestStore.sort = value),
})

const invoiceListSortOrder = computed({
  get: () => requestStore.sortOrder,
  set: (value) => (requestStore.sortOrder = value),
})

const invoiceListSize = computed({
  get: () => requestStore.size,
  set: (value: number) => {
    cookies.cookies.set(INVOICE_LIST_SIZE, String(value))
    requestStore.size = value
  },
})

const invoiceListCompanyInfosId = computed({
  get: () =>
    requestStore.companyInfosId ??
    companyIntegrations.value.find(
      ({ isParent }) => isParent === IsParentCompany.PARENT
    )?.companyInfosId ??
    0,
  set: (value) => (requestStore.companyInfosId = value),
})

const csvDownloadRequest = computed(() => {
  return {
    sort: requestStore.sort,
    sortOrder: requestStore.sortOrder,
    freeWord: requestStore.freeWord,
    invNo: requestStore.invNo,
    dataType: requestStore.dataType,
    companyName: requestStore.companyName,
    fromIssueDate: requestStore.fromIssueDate,
    toIssueDate: requestStore.toIssueDate,
    payDueDate: requestStore.payDueDate,
    fromInvAmount: requestStore.fromInvAmount,
    toInvAmount: requestStore.toInvAmount,
    paymentMethod: requestStore.paymentMethod,
    isOpen: requestStore.isOpen,
    isDownload: requestStore.isDownload,
    isConfirmation: requestStore.isConfirmation,
    companyInfosId: requestStore.companyInfosId,
    fromReceiveDateTime: requestStore.fromReceiveDateTime,
    toReceiveDateTime: requestStore.toReceiveDateTime,
  }
})

// 請求書一覧取得
const getInvoices = async () => {
  apiProgressStore.invoices = true
  const { payload } = await infoApi.getInvoices(requestStore.getRequest)
  requestStore.setRequested()
  apiProgressStore.invoices = false

  pages.value = payload.pages
  total.value = payload.total
  invoices.value = payload.items
  lastReceiveDateTime.value = getDistanceToNow(payload.lastReceiveDateTime)
}

// CSVダウンロード
const getCsv = async () => {
  apiProgressStore.csv = true
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  // CSVダウンロードチェック
  const getCsvCheck = await downloadApi.getInvoiceDownloadsCsvChecks(
    csvDownloadRequest.value
  )
  csvCheckPeppolIds.value = getCsvCheck.payload
  // CsvCheckでPeppolIDが取得出来たらエラー
  if (csvCheckPeppolIds.value.length) {
    apiProgressStore.csv = false
    isCsvErrorActive.value = true
    return
  }

  const response = await downloadApi.getInvoiceDownloadsCsvs(
    csvDownloadRequest.value
  )
  apiProgressStore.csv = false
  const fileName = `invoice_${getCurrentDateTime()}.csv`
  createDownloadFile(response, fileName)
}

// 請求書受取依頼
const postReceive = async () => {
  apiProgressStore.receive = true
  await receiveApi.postInvoicesReceives()
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  invoiceListPage.value = 1
  await getInvoices()
  apiProgressStore.receive = false
}

// 統合企業情報取得
const getCompanyIntegrations = async () => {
  const response = await integrationApi.getCompanyIntegrations()
  companyIntegrations.value = response.payload
}

// 400エラーモーダル
const close400ErrorDialog = () => {
  is400ErrorActive.value = false
  errorDialogStore.setErrorDialog(false)
}

// 検索フォーム
const formEmit = async () => {
  apiProgressStore.invoicesSearch = true
  invoiceListPage.value = 1
  await getInvoices()
  apiProgressStore.invoicesSearch = false
}

// 請求書一覧のページネーション処理
const paginationList = (page: number) => {
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  invoiceListPage.value = page
  getInvoices()
}

// 請求書一覧のソート処理
const sortList = (sort: GetInvoicesSortEnum) => {
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  invoiceListPage.value = 1

  // １回目または前回とソートする項目が違う場合
  if (invoiceListSort.value !== sort) {
    invoiceListSort.value = sort
    invoiceListSortOrder.value = GetInvoicesSortOrderEnum.ASC
    getInvoices()
    return
  }

  // 前回と同様の項目をソートする場合
  if (invoiceListSortOrder.value === GetInvoicesSortOrderEnum.ASC) {
    invoiceListSortOrder.value = GetInvoicesSortOrderEnum.DESC
  } else {
    invoiceListSortOrder.value = GetInvoicesSortOrderEnum.ASC
  }
  getInvoices()
}

// 詳細ページ遷移
const transitionInfo = (invoice: InvoiceListData) => {
  openStore.isOpen = invoice.isOpen
  router.push({
    name: ROUTE_NAMES.INVOICE_DETAIL,
    params: { invoice_id: invoice.invoiceId },
  })
}

// CSVダウンロード
const csvDownload = () => {
  csvCheckPeppolIds.value = []
  if (!total.value) {
    isCsvErrorActive.value = true
    return
  }
  getCsv()
}

const closeCsvErrorDialog = () => {
  isCsvErrorActive.value = false
  errorDialogStore.receiveApi500Error = false
}

// 表示件数モーダル表示処理
const openSizeDialog = () => {
  isSizeDialogActive.value = true
}
const closeSizeDialog = () => {
  isSizeDialogActive.value = false
}
const confirmSize = (confirmSize: number) => {
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  invoiceListPage.value = 1
  invoiceListSize.value = confirmSize
  getInvoices()
  isSizeDialogActive.value = false
}

// 一覧に表示する企業変更
const changeCompany = (companyInfosId: number) => {
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  invoiceListPage.value = 1
  invoiceListCompanyInfosId.value = companyInfosId
  getInvoices()
}

// APIを同期的に取得
const getApi = async () => {
  // 今回検索条件がバリデーションエラーの可能性があるため、前回検索条件で上書きする
  requestStore.setRequest()
  await getInvoices()
  await getCompanyIntegrations()
  loadingStore.loading = false
}

getApi()
</script>

<style lang="scss" scoped></style>
