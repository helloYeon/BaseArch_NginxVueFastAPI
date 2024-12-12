<template>
  <v-container class="pb-16">
    <PageTitle title="請求書情報" />
    <InvoiceDetailHeader
      v-model:confirmation="invoice.isConfirmation"
      v-model:download="invoice.isDownload"
      class="mt-5"
      :invoice="invoice"
      @change-confirm-emit="changeConfirmEmit"
    />
    <v-row align="center" class="mt-5">
      <v-col>
        <v-tabs v-model="tab" color="#B11048">
          <v-tab
            width="160"
            value="invoice"
            size="x-large"
            text="請求情報"
            class="invoice-detail__tab"
          />
          <v-tab
            v-if="
              invoice.currencyCode === JPY_CURRENCY.CODE ||
              invoice.currencyCode === USD_CURRENCY.CODE
            "
            width="160"
            value="preview"
            text="プレビュー"
            class="invoice-detail__tab"
          />
          <v-tab
            width="160"
            value="peppol"
            text="Peppol詳細"
            class="invoice-detail__tab"
          />
        </v-tabs>
      </v-col>
      <v-col v-if="tab === 'peppol'" cols="auto">
        <v-btn
          prepend-icon="mdi-download"
          color="#B11048"
          size="x-large"
          density="compact"
          :loading="apiProgressStore.xml"
          @click="getXml"
        >
          XMLダウンロード
        </v-btn>
      </v-col>
    </v-row>
    <v-divider />

    <v-window v-model="tab">
      <v-window-item value="invoice">
        <InvoiceDetailTab :invoice="invoice" />
      </v-window-item>

      <v-window-item value="preview">
        <InvoiceDetailPreviewTab :pdf-data="pdf" @download="downloadEmit" />
      </v-window-item>

      <v-window-item value="peppol">
        <InvoiceDetailPeppolTab
          v-model:peppol="peppol"
          @open-dialog="openDialog"
        />
      </v-window-item>
    </v-window>
  </v-container>
  <CommonBackOnlyFooter />
  <InvoiceDetailDialog
    v-model:is-active="isActive"
    :invoice-detail="invoiceDetail"
    @close-dialog="closeDialog"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  InfoApi,
  DownloadApi,
  StatusApi,
  Invoice,
  Preview,
  Peppol,
  Detail,
  DataType,
  IsConfirmation,
  GetInvoicesInvoiceIdRequest,
  GetInvoicesDownloadsPreviewsInvoiceIdRequest,
  GetInvoicesPeppolInvoiceIdRequest,
  GetInvoicesDetailsInvoiceDetailIdRequest,
  PutInvoicesStatusConfirmRequest,
  PutInvoiceStatusConfirm,
  IsDownload,
  PutInvoiceStatusDownload,
  PutInvoicesStatusDownloadRequest,
  GetInvoiceDownloadsXmlsRequest,
  IsOpen,
  PutInvoiceStatusOpen,
  PutInvoicesStatusOpenRequest,
} from '@/codegen'
import { ClientConfig } from '@/plugins/apiClient'
import CommonBackOnlyFooter from '@/components/templates/Common/CommonBackOnlyFooter.vue'
import PageTitle from '@/components/parts/PageTitle.vue'
import InvoiceDetailHeader from '@/components/templates/InvoiceDetail/InvoiceDetailHeader.vue'
import InvoiceDetailTab from '@/components/templates/InvoiceDetail/InvoiceDetailTab.vue'
import InvoiceDetailPreviewTab from '@/components/templates/InvoiceDetail/InvoiceDetailPreviewTab.vue'
import InvoiceDetailPeppolTab from '@/components/templates/InvoiceDetail/InvoiceDetailPeppolTab.vue'
import InvoiceDetailDialog from '@/components/templates/InvoiceDetail/InvoiceDetailDialog.vue'
import { createDownloadFile, getCurrentDateTime } from '@/plugins/utils'
import { useApiProgressStore } from '@/store/apiProgress'
import { useOpenStore } from '@/store/open'
import { JPY_CURRENCY, USD_CURRENCY } from '@/const/const'
import { useLoadingStore } from '@/store/loading'

const apiProgressStore = useApiProgressStore()
const openStore = useOpenStore()
const loadingStore = useLoadingStore()

const route = useRoute()

const infoApi = new InfoApi(new ClientConfig())
const downloadApi = new DownloadApi(new ClientConfig())
const statusApi = new StatusApi(new ClientConfig())

const tab = ref('invoice')
const invoice = ref<Invoice>(<Invoice>{})
const pdf = ref<Preview>(<Preview>{})
const peppol = ref<Peppol>(<Peppol>{})
const invoiceDetail = ref<Detail>(<Detail>{})
const isActive = ref(false)

// 請求書取得
const getInvoice = async () => {
  const getInvoiceInvoiceIdRequest: GetInvoicesInvoiceIdRequest = {
    invoiceId: Number(route.params.invoice_id),
  }
  const response = await infoApi.getInvoicesInvoiceId(
    getInvoiceInvoiceIdRequest
  )

  invoice.value = response.payload
}

// プレビュー用請求書取得
const getPreview = async () => {
  const getInvoicesDownloadsPreviewsInvoiceIdRequest: GetInvoicesDownloadsPreviewsInvoiceIdRequest =
    {
      invoiceId: Number(route.params.invoice_id),
    }
  const response = await downloadApi.getInvoicesDownloadsPreviewsInvoiceId(
    getInvoicesDownloadsPreviewsInvoiceIdRequest
  )

  pdf.value = response.payload
}

// XMLダウンロード
const getXml = async () => {
  apiProgressStore.xml = true
  const getInvoicesPeppolInvoiceIdRequest: GetInvoiceDownloadsXmlsRequest = {
    invoiceId: Number(route.params.invoice_id),
  }
  const response = await downloadApi.getInvoiceDownloadsXmls(
    getInvoicesPeppolInvoiceIdRequest
  )

  const fileName = `${invoice.value.dataType !== DataType.PURCHASESTATEMENT ? '請求書' : '通知書'}_${getCurrentDateTime()}`
  createDownloadFile(response, fileName)
  apiProgressStore.xml = false
}

// Peppol詳細取得
const getPeppol = async () => {
  const getInvoicesPeppolInvoiceIdRequest: GetInvoicesPeppolInvoiceIdRequest = {
    invoiceId: Number(route.params.invoice_id),
  }
  const response = await infoApi.getInvoicesPeppolInvoiceId(
    getInvoicesPeppolInvoiceIdRequest
  )

  peppol.value = response.payload
}

// 請求書明細取得
const getInvoiceDetails = async (invoiceDetailId: number) => {
  const getInvoiceDetailsRequest: GetInvoicesDetailsInvoiceDetailIdRequest = {
    invoiceDetailId: invoiceDetailId,
  }
  apiProgressStore.detail = true
  const response = await infoApi.getInvoicesDetailsInvoiceDetailId(
    getInvoiceDetailsRequest
  )
  apiProgressStore.detail = false
  invoiceDetail.value = response.payload
}

// 開封ステータス更新
const putStatusOpen = async () => {
  if (openStore.isOpen === IsOpen.OPENED) return

  const putInvoiceStatusOpen: PutInvoiceStatusOpen = {
    invoiceId: Number(route.params.invoice_id),
    isOpen: IsOpen.OPENED,
  }
  const putInvoicesStatusOpenRequest: PutInvoicesStatusOpenRequest = {
    putInvoiceStatusOpen: putInvoiceStatusOpen,
  }
  await statusApi.putInvoicesStatusOpen(putInvoicesStatusOpenRequest)
}

// 確認ステータス更新
const putStatusConfirm = async (isConfirmation: IsConfirmation) => {
  const putInvoiceStatusConfirm: PutInvoiceStatusConfirm = {
    invoiceId: Number(route.params.invoice_id),
    isConfirmation: isConfirmation,
  }
  const putInvoicesStatusConfirmationRequest: PutInvoicesStatusConfirmRequest =
    {
      putInvoiceStatusConfirm: putInvoiceStatusConfirm,
    }
  apiProgressStore.confirm = true
  await statusApi.putInvoicesStatusConfirm(putInvoicesStatusConfirmationRequest)
  apiProgressStore.confirm = false
}

// ダウンロードステータス更新
const putStatusDownload = async () => {
  const putInvoiceStatusDownload: PutInvoiceStatusDownload = {
    invoiceId: Number(route.params.invoice_id),
    isDownload: IsDownload.DOWNLOADED,
  }
  const putInvoiceStatusDownloadRequest: PutInvoicesStatusDownloadRequest = {
    putInvoiceStatusDownload: putInvoiceStatusDownload,
  }
  apiProgressStore.download = true
  await statusApi.putInvoicesStatusDownload(putInvoiceStatusDownloadRequest)
  apiProgressStore.download = false
}

// 確認ステータス更新処理
const changeConfirmEmit = (isConfirmation: IsConfirmation) => {
  putStatusConfirm(isConfirmation)
}

// PDFダウンロード処理
const downloadEmit = async (pdfData: Blob) => {
  const fileName = `${pdf.value.dataType !== DataType.PURCHASESTATEMENT ? '請求書' : '通知書'}_${getCurrentDateTime()}.pdf`
  await createDownloadFile(pdfData, fileName)

  if (invoice.value.isDownload === IsDownload.UNDOWNLOADED) {
    await putStatusDownload()
    invoice.value.isDownload = IsDownload.DOWNLOADED
  }
}

// 請求書明細ポップアップ処理
const openDialog = async (id: number) => {
  if (apiProgressStore.detail) return
  await getInvoiceDetails(id)
  isActive.value = true
}
const closeDialog = () => {
  isActive.value = false
}

// APIを同期的に取得
const getApi = async () => {
  await getInvoice()
  await getPreview()
  await getPeppol()
  await putStatusOpen()
  loadingStore.loading = false
}

getApi()
</script>

<style lang="scss" scoped>
.invoice-detail__tab {
  font-size: 1.4rem;
  font-weight: bold;
  color: #222222;
  text-transform: none;
}
</style>
