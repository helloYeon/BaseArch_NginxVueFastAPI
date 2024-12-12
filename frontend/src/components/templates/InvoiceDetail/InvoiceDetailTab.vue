<template>
  <InvoiceDetailTabCommonContent title="基本情報">
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">発行日</p>
      </v-col>
      <v-col cols="4">
        <p class="value-col">
          {{ formatDate(invoice.listInfo?.sendDate) }}
        </p>
      </v-col>
      <v-col cols="2">
        <p class="font-weight-bold">請求書タイプ</p>
      </v-col>
      <v-col cols="4">
        <p>{{ dataTypeTitle(invoice.dataType) }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">送信者ID</p>
      </v-col>
      <v-col cols="4">
        <p class="value-col">
          {{ invoice.publisher?.publisherPeppolId }}
        </p>
      </v-col>
      <v-col cols="2">
        <p class="font-weight-bold">受信者ID</p>
      </v-col>
      <v-col cols="4">
        <p>{{ invoice.customer?.peppolId }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">添付ファイル</p>
      </v-col>
      <v-col>
        <p
          v-for="item in invoice.sellerAttachedFile"
          :key="item.fileName"
          class="value-col"
        >
          <template v-if="item.fileName">
            {{ item.fileName }} [<a
              class="link"
              @click="downloadFile(item.fileName, item.file)"
              >{{ getExtension(item.fileName) }}</a
            >]
          </template>
        </p>
      </v-col>
    </v-row>
    <v-row class="row align-center">
      <v-col cols="2">
        <p class="font-weight-bold">備考</p>
      </v-col>
      <v-col>
        <p class="value-col">
          {{ invoice.remarks }}
        </p>
      </v-col>
    </v-row>
  </InvoiceDetailTabCommonContent>
  <InvoiceDetailTabCommonContent title="請求金額">
    <v-row>
      <v-col class="pa-0">
        <v-expansion-panels v-model="panel" class="panels">
          <v-expansion-panel selected-class=".selected">
            <div class="d-flex row row-border">
              <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                <div
                  class="col-border d-flex justify-space-between align-center w-100 pr-8"
                >
                  <p class="font-weight-bold">今回請求金額 (税抜)</p>
                  <p v-if="invoice.invWithoutTax !== null" class="value-col">
                    {{
                      currencyMark(invoice.currencyCode) +
                      numToStrNum(invoice.invWithoutTax)
                    }}
                  </p>
                </div>
                <div
                  class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                >
                  <p class="font-weight-bold">今回消費税額</p>
                  <p v-if="invoice.invTax !== null" class="value-col">
                    {{
                      currencyMark(invoice.currencyCode) +
                      numToStrNum(invoice.invTax)
                    }}
                  </p>
                </div>
                <div
                  class="d-flex justify-space-between align-center w-100 pl-8"
                >
                  <p class="font-weight-bold">今回請求金額 (税込)</p>
                  <p v-if="invoice.invAmount !== null" class="value-col">
                    {{
                      currencyMark(invoice.currencyCode) +
                      numToStrNum(invoice.invAmount)
                    }}
                  </p>
                </div>
              </v-col>
              <v-col
                class="d-flex align-center justify-end pa-0 panel-button"
                @click="panelButton"
              >
                <v-icon :icon="iconComputed" size="18" />
                <p class="panel-button__text">内訳</p>
              </v-col>
            </div>
            <v-expansion-panel-text>
              <v-row v-if="invoice.invAmountTr10" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (10%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxTr10)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (10%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxTr10)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (10%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountTr10)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountTr8Reduced" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (軽減8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxTr8Reduced)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (軽減8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxTr8Reduced)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (軽減8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountTr8Reduced)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountTr8" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxTr8)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxTr8)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (8%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountTr8)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountTr5" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (5%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxTr5)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (5%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxTr5)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (5%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountTr5)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountTr0" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (0%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxTr0)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (0%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxTr0)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (0%対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountTr0)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountFree" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (非課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxFree)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (非課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxFree)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (非課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountFree)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountNon" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (不課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxNon)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (不課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxNon)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (不課税)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountNon)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
              <v-row v-if="invoice.invAmountExemption" class="row row-border">
                <v-col cols="11" class="d-flex justify-space-between pa-0 ma-3">
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8"
                  >
                    <p>税抜金額 (免税対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invWithoutTaxExemption)
                      }}
                    </p>
                  </div>
                  <div
                    class="col-border d-flex justify-space-between align-center w-100 pr-8 pl-8"
                  >
                    <p>消費税額 (免税対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invTaxExemption)
                      }}
                    </p>
                  </div>
                  <div
                    class="d-flex justify-space-between align-center w-100 pl-8"
                  >
                    <p>合計 (免税対象)</p>
                    <p class="value-col">
                      {{
                        currencyMark(invoice.currencyCode) +
                        numToStrNum(invoice.invAmountExemption)
                      }}
                    </p>
                  </div>
                </v-col>
              </v-row>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">支払済み金額 (税抜)</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">金額</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!invoice.paidInfo" :columns="2" />
          <tbody v-for="(item, index) in invoice.paidInfo" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td v-if="item.paidWithoutTax !== undefined" class="text-right">
                {{
                  currencyMark(invoice.currencyCode) +
                  numToStrNum(item.paidWithoutTax)
                }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">返金金額 (税抜き)</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">金額</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!invoice.refundInfo" :columns="2" />
          <tbody v-for="(item, index) in invoice.refundInfo" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td v-if="item.refundWithoutTax !== undefined" class="text-right">
                {{
                  currencyMark(invoice.currencyCode) +
                  numToStrNum(item.refundWithoutTax)
                }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">追加請求金額 (税抜き)</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">金額</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!invoice.additionalInfo" :columns="2" />
          <tbody v-for="(item, index) in invoice.additionalInfo" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td
                v-if="item.additionalWithoutTax !== undefined"
                class="text-right"
              >
                {{
                  currencyMark(invoice.currencyCode) +
                  numToStrNum(item.additionalWithoutTax)
                }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </InvoiceDetailTabCommonContent>
  <InvoiceDetailTabCommonContent title="明細情報">
    <v-row>
      <v-col>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">ID</th>
              <th class="font-weight-bold text-center">文書ID</th>
              <th class="font-weight-bold text-center">品名</th>
              <th class="font-weight-bold text-center">明細日付</th>
              <th class="font-weight-bold text-center">数量</th>
              <th class="font-weight-bold text-center">単位</th>
              <th class="font-weight-bold text-center">
                値引き前単価<span class="tax"> (税抜)</span>
              </th>
              <th class="font-weight-bold text-center">
                値引き後単価<span class="tax"> (税抜)</span>
              </th>
              <th class="font-weight-bold text-center">
                値引き後金額<span class="tax"> (税抜)</span>
              </th>
              <th class="font-weight-bold text-center">消費税額</th>
              <th class="font-weight-bold text-center">
                合計金額<span class="tax"> (税込)</span>
              </th>
              <th class="font-weight-bold text-center">備考</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!invoice.details" :columns="13" />
          <tbody v-for="(item, index) in invoice.details" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td class="text-right">
                {{ item.itemSlipNo }}
              </td>
              <td>
                {{ item.itemProdCode }}
              </td>
              <td>{{ item.itemName }}</td>
              <td class="text-right">
                {{ formatDate(item.itemSlipDate) }}
              </td>
              <td class="text-right">
                {{ item.itemQty }}
              </td>
              <td>
                {{ item.itemUnit }}
              </td>
              <td class="text-right" />
              <td class="text-right">
                <span v-if="item.itemPrice !== undefined">
                  {{
                    currencyMark(invoice.currencyCode) +
                    numToStrNum(item.itemPrice)
                  }}
                </span>
              </td>
              <td class="text-right">
                <span v-if="item.itemWithoutTax !== undefined">
                  {{ formatPrice(invoice.currencyCode, item.itemWithoutTax) }}
                </span>
              </td>
              <td class="text-right">
                <p class="consumption-tax">
                  <span v-if="item.itemTax !== undefined">
                    {{ formatPrice(invoice.currencyCode, item.itemTax) }}
                  </span>
                  <br />
                  <span v-if="item.taxType === TaxType.TAX">
                    課税
                    <span v-if="item.reducedTaxFlg === ReducedTaxFlg.REDUCED">
                      軽減 </span
                    >{{ item.taxRateSec }}%
                  </span>
                  <span v-if="item.taxType === TaxType.TAXFREE"> 非課税 </span>
                  <span v-if="item.taxType === TaxType.TAXEXEMPTION">
                    免税
                  </span>
                  <span v-if="item.taxType === TaxType.TAXNON"> 不課税 </span>
                </p>
              </td>
              <td class="text-right">
                <span
                  v-if="
                    item.itemWithoutTax !== undefined &&
                    item.itemTax !== undefined
                  "
                >
                  {{
                    formatPrice(
                      invoice.currencyCode,
                      (item.itemWithoutTax ?? 0) + (item.itemTax ?? 0)
                    )
                  }}
                </span>
              </td>
              <td>{{ item.detailRemarks }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </InvoiceDetailTabCommonContent>
  <InvoiceDetailTabCommonContent title="請求詳細">
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">請求元法人ID</p>
      </v-col>
      <v-col cols="4">
        <p class="value-col">
          {{ invoice.iBG04?.aUTO13?.aUTO25?.iBT030?.value }}
        </p>
      </v-col>
      <v-col cols="2">
        <p class="font-weight-bold">請求元税ID</p>
      </v-col>
      <v-col cols="4">
        <p>{{ invoice.iBG04?.aUTO13?.aUTO20?.iBT031 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">請求元電子アドレス</p>
      </v-col>
      <v-col>
        <p class="value-col">
          {{ invoice.iBG04?.aUTO13?.iBT034?.value }}
        </p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">買い手(購入者)名称</p>
      </v-col>
      <v-col cols="4">
        <p class="value-col">
          {{ invoice.iBG07?.aUTO26?.aUTO33?.iBT044 }}
        </p>
      </v-col>
      <v-col cols="2">
        <p class="font-weight-bold">買い手(購入者)法人ID</p>
      </v-col>
      <v-col cols="4">
        <p>{{ invoice.iBG07?.aUTO26?.aUTO33?.iBT047?.value }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">買い手(購入者)税ID</p>
      </v-col>
      <v-col cols="4">
        <p class="value-col">
          {{ invoice.iBG07?.aUTO26?.aUTO31?.iBT048 }}
        </p>
      </v-col>
      <v-col cols="2">
        <p class="font-weight-bold">買い手(購入者)<br />電子アドレス</p>
      </v-col>
      <v-col cols="4">
        <p>{{ invoice.iBG07?.aUTO26?.iBT049?.value }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border align-center">
      <v-col cols="2">
        <p class="font-weight-bold">買い手(購入者)住所</p>
      </v-col>
      <v-col>
        <p class="value-col">
          {{
            `${invoice.iBG07?.aUTO26?.iBG08?.iBT053 ?? ''} ${invoice.iBG07?.aUTO26?.iBG08?.iBT054 ?? ''}${invoice.iBG07?.aUTO26?.iBG08?.iBT052 ?? ''}${invoice.iBG07?.aUTO26?.iBG08?.iBT050 ?? ''}${invoice.iBG07?.aUTO26?.iBG08?.iBT051 ?? ''}${invoice.iBG07?.aUTO26?.iBG08?.aUTO29?.iBT163 ?? ''}`
          }}
        </p>
      </v-col>
    </v-row>
  </InvoiceDetailTabCommonContent>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import InvoiceDetailTabCommonContent from '@/components/templates/InvoiceDetail/InvoiceDetailTabCommonContent.vue'
import CommonEmptyTableRow from '@/components/templates/Common/CommonEmptyTableRow.vue'
import { Invoice, ReducedTaxFlg, TaxType } from '@/codegen'
import {
  formatDate,
  dataTypeTitle,
  numToStrNum,
  createDownloadFile,
  currencyMark,
  formatPrice,
} from '@/plugins/utils'

interface InvoiceProps {
  invoice: Invoice
}

defineProps<InvoiceProps>()

const panel = ref<number[]>([])

const icon = ref('mdi-plus-box-outline')
const iconComputed = computed(() => {
  return icon.value
})

// ファイル名から拡張子名取得
const getExtension = (fileName: string | undefined) => {
  return fileName?.split('.').pop()
}

// Base64からBlob形式へ変換
const base64toBlob = (base64: string): Blob => {
  const decodedFile = atob(base64.replace(/^.*,/, ''))
  const buffer = new Uint8Array(decodedFile.length)
  for (let i = 0; i < decodedFile.length; i++) {
    buffer[i] = decodedFile.charCodeAt(i)
  }

  return new Blob([buffer.buffer])
}

// ファイルダウンロード
const downloadFile = (
  fileName: string | undefined,
  file: string | undefined
) => {
  if (!fileName || !file) return null

  const blob = base64toBlob(file)
  createDownloadFile(blob, fileName)
}

const panelButton = () => {
  if (panel.value.length) {
    panel.value = []
    icon.value = 'mdi-plus-box-outline'
    return
  }
  icon.value = 'mdi-minus-box-outline'
  panel.value.push(0)
}
</script>

<style lang="scss" scoped>
p {
  font-size: 12px;
}
.row {
  color: #222222;
  min-height: 60px;
}
.row-border {
  border-bottom: 2px solid #e0e0e0;
}
.col-border {
  border-right: 2px solid #e0e0e0;
}
.value-col {
  font-size: 1.3rem;

  & .link {
    color: #b11048;
    cursor: pointer;
  }
}

.panels {
  margin-top: 5px;
  box-shadow: none;
}
.panel-button {
  color: #b11048;
  cursor: pointer;

  &__text {
    font-size: 1.4rem;
  }
}

.v-expansion-panels {
  // パネルの影削除
  :deep(.v-expansion-panel__shadow) {
    box-shadow: none;
  }
  // TextパネルのPadding変更
  :deep(.v-expansion-panel-text__wrapper) {
    padding: 8px 12px 8px;
  }
}

.table {
  font-size: 1.3rem;
  color: #222222;
  width: 100%;

  & .table-header {
    background-color: #f6f6f6;
  }

  &,
  th,
  td {
    border-collapse: collapse;
    border: 1px solid #e0e0e0;
    white-space: nowrap;
  }

  & .index {
    width: 30px;
  }
  & .tax {
    font-size: 1rem;
  }
  & .consumption-tax {
    line-height: 1;
  }
}
</style>
