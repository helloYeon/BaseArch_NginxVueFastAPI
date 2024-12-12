<template>
  <v-dialog v-model="isActiveComputed" width="80%" scrollable>
    <v-card>
      <v-card-item class="header">
        <v-card-title class="title d-flex justify-space-between align-center">
          <h1>請求書明細行</h1>
          <v-btn icon variant="text" @click="emit('closeDialog')">
            <v-icon icon="mdi-close" size="28" color="#B11048" />
          </v-btn>
        </v-card-title>
      </v-card-item>
      <v-card-text>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行ID</p>
            <p>{{ invoiceDetail.iBT126 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行注釈</p>
            <p>{{ invoiceDetail.iBT127 }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">明細行文書ID</p>
            <p>{{ invoiceDetail.iBG36?.iBT188 }}</p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">文書タイプコード</p>
            <p>{{ invoiceDetail.iBG36?.iBT189 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行オブジェクトID</p>
            <p>{{ invoiceDetail.aUTO87?.iBT128?.value }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行オブジェクト スキーマID</p>
            <p>{{ invoiceDetail.aUTO87?.iBT128?.schemeID }}</p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求する数量</p>
            <p>{{ invoiceDetail.iBT129.value }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求する数量の数量単位コード</p>
            <p>{{ invoiceDetail.iBT129.unitCode }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">値引後請求明細行金額(税抜)</p>
            <p>
              {{ strNumToLocaleStringNum(invoiceDetail.iBT131.value) }}
            </p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">購買発注書参照</p>
            <p>{{ invoiceDetail.aUTO82?.aUTO83?.iBT183 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">購買発注明細行参照</p>
            <p>{{ invoiceDetail.aUTO82?.iBT132 }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">出荷案内書参照</p>
            <p>{{ invoiceDetail.aUTO84?.aUTO86?.iBT184 }}</p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行買い手会計参照</p>
            <p>{{ invoiceDetail.iBT133 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行の期間開始日</p>
            <p>{{ invoiceDetail.iBG26?.iBT134 }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">請求書明細行の期間終了日</p>
            <p>{{ invoiceDetail.iBG26?.iBT135 }}</p>
          </v-col>
        </v-row>
        <v-row>
          <p class="sub-title mt-8">請求書明細行の返金</p>
          <v-col>
            <v-table class="table" density="compact">
              <thead class="table-header">
                <tr>
                  <th />
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />返金金額(税抜)
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />返金金額の基準金額
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />返金の率
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />返金理由
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />返金の理由コード
                  </th>
                </tr>
              </thead>
              <CommonEmptyTableRow v-if="!invoiceDetail.iBG27" :columns="6" />
              <tbody v-for="(item, index) in invoiceDetail.iBG27" :key="index">
                <tr>
                  <td class="font-weight-bold text-center index">
                    {{ index + 1 }}
                  </td>
                  <td class="text-right">
                    {{ strNumToLocaleStringNum(item.iBT136?.value) }}
                  </td>
                  <td class="text-right">
                    {{ strNumToLocaleStringNum(item.iBT137?.value) }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT138 }}
                  </td>
                  <td>
                    {{ item.iBT139 }}
                  </td>
                  <td>
                    {{ item.iBT140 }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <p class="sub-title mt-8">請求書明細行の追加請求</p>
          <v-col>
            <v-table class="table" density="compact">
              <thead class="table-header">
                <tr>
                  <th />
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />追加請求金額(税抜)
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />追加請求の基準金額
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />追加請求の率
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />追加請求理由
                  </th>
                  <th class="font-weight-bold text-center">
                    請求書明細行の<br />追加請求理由コード
                  </th>
                </tr>
              </thead>
              <CommonEmptyTableRow v-if="!invoiceDetail.iBG28" :columns="6" />
              <tbody v-for="(item, index) in invoiceDetail.iBG28" :key="index">
                <tr>
                  <td class="font-weight-bold text-center index">
                    {{ index + 1 }}
                  </td>
                  <td class="text-right">
                    {{ strNumToLocaleStringNum(item.iBT141?.value) }}
                  </td>
                  <td class="text-right">
                    {{ strNumToLocaleStringNum(item.iBT142?.value) }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT143 }}
                  </td>
                  <td>
                    {{ item.iBT144 }}
                  </td>
                  <td>
                    {{ item.iBT145 }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <p class="sub-title mt-8">品目情報</p>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品名</p>
            <p>{{ invoiceDetail.iBG31.iBT153 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目摘要</p>
            <p>{{ invoiceDetail.iBG31.iBT154 }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">売り手による品目ID</p>
            <p>{{ invoiceDetail.iBG31.aUTO96?.iBT155 }}</p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">買い手による品目ID</p>
            <p>{{ invoiceDetail.iBG31.aUTO95?.iBT156 }}</p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目標準ID</p>
            <p>{{ invoiceDetail.iBG31.aUTO97?.iBT157?.value }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">品目標準ID スキーマID</p>
            <p>{{ invoiceDetail.iBG31.aUTO97?.iBT157?.schemeID }}</p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目の原産国</p>
            <p>{{ invoiceDetail.iBG31.aUTO98?.iBT159 }}</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="font-weight-bold mb-3">品目分類</p>
            <v-table class="table" density="compact">
              <thead class="table-header">
                <tr>
                  <th />
                  <th class="font-weight-bold text-center">品目分類ID</th>
                  <th class="font-weight-bold text-center">
                    品目分類ID スキーマID
                  </th>
                  <th class="font-weight-bold text-center">
                    品目分類IDスキーマのバージョンID
                  </th>
                </tr>
              </thead>
              <CommonEmptyTableRow
                v-if="!invoiceDetail.iBG31.aUTO99"
                :columns="4"
              />
              <tbody
                v-for="(item, index) in invoiceDetail.iBG31.aUTO99"
                :key="index"
              >
                <tr>
                  <td class="font-weight-bold text-center index">
                    {{ index + 1 }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT158?.value }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT158?.listID }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT158?.listVersionID }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="font-weight-bold mb-3">請求書明細行税情報</p>
            <v-table class="table" density="compact">
              <thead class="table-header">
                <tr>
                  <th />
                  <th class="font-weight-bold text-center">
                    請求する品目に対する課税分類コード
                  </th>
                  <th class="font-weight-bold text-center">
                    請求する品目に対する税率
                  </th>
                  <th class="font-weight-bold text-center">
                    請求する品目に対する単位数量当たりの税金額
                  </th>
                  <th class="font-weight-bold text-center">税スキーマ</th>
                </tr>
              </thead>
              <CommonEmptyTableRow
                v-if="!invoiceDetail.iBG31.iBG30"
                :columns="5"
              />
              <tbody
                v-for="(item, index) in invoiceDetail.iBG31.iBG30"
                :key="index"
              >
                <tr>
                  <td class="font-weight-bold text-center index">
                    {{ index + 1 }}
                  </td>
                  <td>
                    {{ item.iBT151 }}
                  </td>
                  <td class="text-right">
                    {{ item.iBT152 }}
                  </td>
                  <td class="text-right">
                    {{ strNumToLocaleStringNum(item.iBT166?.value) }}
                  </td>
                  <td>
                    {{ item.aUTO101?.iBT167 }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="font-weight-bold mb-3">品目属性</p>
            <v-table class="table" density="compact">
              <thead class="table-header">
                <tr>
                  <th />
                  <th class="font-weight-bold text-center">品目属性名</th>
                  <th class="font-weight-bold text-center">品目属性値</th>
                </tr>
              </thead>
              <CommonEmptyTableRow
                v-if="!invoiceDetail.iBG31.iBG32"
                :columns="3"
              />
              <tbody
                v-for="(item, index) in invoiceDetail.iBG31.iBG32"
                :key="index"
              >
                <tr>
                  <td class="font-weight-bold text-center index">
                    {{ index + 1 }}
                  </td>
                  <td>
                    {{ item.iBT160 }}
                  </td>
                  <td>
                    {{ item.iBT161 }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <p class="sub-title mt-8">取引価格詳細</p>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目単価(値引後)(税抜き)</p>
            <p>
              {{ strNumToLocaleStringNum(invoiceDetail.iBG29.iBT146?.value) }}
            </p>
          </v-col>
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目単価値引(税抜)</p>
            <p>
              {{
                strNumToLocaleStringNum(
                  invoiceDetail.iBG29.aUTO103?.iBT147?.value
                )
              }}
            </p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">品目単価(値引前)(税抜き)</p>
            <p>
              {{
                strNumToLocaleStringNum(
                  invoiceDetail.iBG29.aUTO103?.iBT148?.value
                ).toLocaleString()
              }}
            </p>
          </v-col>
        </v-row>
        <v-row class="row row-border">
          <v-col class="col-border pa-0 ma-3">
            <p class="font-weight-bold">品目単価基準数量</p>
            <p>{{ invoiceDetail.iBG29.iBT149?.value }}</p>
          </v-col>
          <v-col class="pa-0 ma-3">
            <p class="font-weight-bold">品目単価基準数量の数量単位コード</p>
            <p>{{ invoiceDetail.iBG29.iBT149?.unitCode }}</p>
          </v-col>
          <v-col class="pa-0 ma-3" />
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { Detail } from '@/codegen'
import { computed } from 'vue'
import { strNumToLocaleStringNum } from '@/plugins/utils'
import CommonEmptyTableRow from '@/components/templates/Common/CommonEmptyTableRow.vue'

interface DialogProps {
  isActive: boolean
  invoiceDetail: Detail
}

interface DialogEmits {
  (e: 'update:isActive', isActive: boolean): void
  (e: 'closeDialog'): void
}

const props = defineProps<DialogProps>()
const emit = defineEmits<DialogEmits>()

const isActiveComputed = computed({
  get: () => props.isActive,
  set: (value: boolean) => {
    emit('update:isActive', value)
  },
})
</script>

<style lang="scss" scoped>
p {
  font-size: 12px;
  color: #222222;
}
.header {
  background-color: #f7efef;

  color: #b11048;
}
.title {
  height: 56px;
  font-size: 0.9rem;
}
.row {
  height: 72px;
  color: #222222;

  & .col-border {
    border-right: 2px solid #e0e0e0;
  }
}
.row-border {
  border-bottom: 2px solid #e0e0e0;
}
.sub-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #222222;
  border-bottom: 2px solid #22222280;
  width: 100%;
  line-height: 4;
}

.table {
  font-size: 1.3rem;
  width: 100%;
  color: #222222;

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
}
</style>
