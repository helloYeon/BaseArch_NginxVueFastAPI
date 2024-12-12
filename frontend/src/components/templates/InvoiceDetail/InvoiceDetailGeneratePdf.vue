<template>
  <div ref="refPrintDom" hidden>
    <p style="text-align: right; font-size: 8pt">出力日：{{ outputDate }}</p>
    <table data-pdfmake='{"layout":"noBorders", "widths":["auto","*","auto"]}'>
      <tr>
        <td />
        <td style="width: 350pt; height: 100pt">
          <h1
            style="
              text-align: center;
              font-size: 19.5pt;
              text-decoration: underline;
              margin-top: 5pt;
            "
          >
            <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
              支払通知書
            </span>
            <span v-else> 請　求　書 </span>
          </h1>
        </td>
        <td />
      </tr>
    </table>
    <table style="font-size: 8pt" data-pdfmake='{"layout":"noBorders"}'>
      <tr>
        <td style="width: 170pt">
          <table style="height: 100%; width: 100%">
            <tr>
              <th
                style="height: 12pt; margin-top: 2pt; background-color: #cccccc"
              >
                <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                  送付先　(コード：{{ pdfData.customer?.privateCustCd }})
                </span>
                <span v-else>請求先</span>
              </th>
            </tr>
            <tr style="height: 155pt">
              <td style="font-size: 7.5pt">
                <table
                  data-pdfmake='{"layout":"noBorders", "widths":["*","auto"]}'
                >
                  <td>
                    <p>〒{{ pdfData.customer?.zip }}</p>
                    <p>{{ customerAddressComputed }}</p>
                    <p style="margin-top: 10pt">
                      TEL：{{ pdfData.customer?.phone }}
                    </p>
                    <p style="font-weight: bold">
                      {{ pdfData.customer?.companyNameOrg }}
                    </p>
                    <span style="text-align: right">御中</span>
                    <span
                      v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
                      style="margin-top: 15pt"
                    >
                      登録番号：{{ pdfData.customer?.taxCorpId }}
                    </span>
                  </td>
                  <td />
                </table>
              </td>
            </tr>
          </table>
        </td>
        <td style="width: 212pt">
          <table style="height: 100%; width: 100%">
            <tr style="height: 12pt; margin-top: 2pt">
              <th style="background-color: #cccccc">
                <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                  送付元　(コード：{{ pdfData.publisher?.publisherMngNum }})
                </span>
                <span v-else>
                  請求元　(支払先コード：{{
                    pdfData.publisher?.publisherMngNum
                  }})
                </span>
              </th>
            </tr>
            <tr style="height: 155pt">
              <td style="font-size: 7.5pt">
                <table
                  data-pdfmake='{"layout":"noBorders", "widths":["*","auto"]}'
                >
                  <td>
                    <p>〒{{ pdfData.publisher?.publisherZip }}</p>
                    <p>{{ publisherAddressComputed }}</p>

                    <p style="margin-top: 10pt">
                      TEL：{{ pdfData.publisher?.publisherPhone }}
                    </p>
                    <p>
                      {{ pdfData.publisher?.publisherCompanyNameOrg }}
                    </p>
                    <p style="margin-top: 25pt">
                      <span
                        v-if="pdfData.dataType !== DataType.ITEMIZEDINVOICE"
                      >
                        登録番号：{{ pdfData.publisher?.publisherTaxCorpId }}
                      </span>
                      <span
                        v-if="pdfData.dataType === DataType.ITEMIZEDINVOICE"
                      >
                        担当：{{ pdfData.contact }}
                      </span>
                    </p>
                  </td>
                  <td />
                </table>
              </td>
            </tr>
          </table>
        </td>
        <td>
          <table style="margin-bottom: 10pt">
            <th
              style="
                height: 12pt;
                width: 50pt;
                background-color: #cccccc;
                font-weight: bold;
              "
            >
              <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                通知日
              </span>
              <span v-else>請求書発行日</span>
            </th>
            <td style="width: 91pt">
              {{ formatDate(pdfData.listInfo?.sendDate, 'yyyy年MM月dd日(E)') }}
            </td>
          </table>
          <table style="margin-bottom: 10pt">
            <th
              style="
                height: 12pt;
                width: 50pt;
                background-color: #cccccc;
                font-weight: bold;
              "
            >
              <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                番号
              </span>
              <span v-else>請求書番号</span>
            </th>
            <td style="width: 91pt">
              {{ pdfData.invNo }}
            </td>
          </table>
          <table style="margin-bottom: 10pt">
            <th
              style="
                height: 12pt;
                width: 50pt;
                background-color: #cccccc;
                font-weight: bold;
              "
            >
              締日
            </th>
            <td style="width: 91pt">
              {{ formatDate(pdfData.closeDate, 'yyyy年MM月dd日(E)') }}
            </td>
          </table>
          <table>
            <th
              style="
                height: 12pt;
                width: 50pt;
                background-color: #cccccc;
                font-weight: bold;
              "
            >
              <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                支払日
              </span>
              <span v-else>支払期限</span>
            </th>
            <td style="width: 91pt">
              {{ formatDate(pdfData.payDueDate, 'yyyy年MM月dd日(E)') }}
            </td>
          </table>
        </td>
      </tr>
    </table>
    <p
      v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT"
      style="font-size: 7.5pt"
    >
      平素は格別のお引立てを贈り、誠にありがとうございます。下記の通りご請求申し上げます。
    </p>
    <table>
      <tr style="font-weight: bold">
        <th
          style="
            font-size: 16pt;
            height: 30pt;
            width: 161pt;
            margin-top: 3pt;
            background-color: #cccccc;
            text-align: left;
          "
        >
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
            通知金額
          </span>
          <span v-else>請求金額</span>
        </th>
        <td style="font-size: 16pt; width: 210pt; margin-top: 3pt">
          <span v-if="pdfData.currencyCode === USD_CURRENCY.CODE">$</span>
          {{ numToStrNum(pdfData.invAmount) }}
          <span v-if="pdfData.currencyCode === JPY_CURRENCY.CODE">円</span>
        </td>
      </tr>
    </table>
    <table>
      <td style="height: 15pt; width: 380pt; font-size: 9pt">
        件名： {{ pdfData.invName }}
      </td>
    </table>
    <p style="font-size: 7.5pt">
      ※BtoBプラットフォーム
      請求書では、通知書送付者のID及び履歴情報保管により、信頼性が担保されています。
    </p>
    <table v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT">
      <tr>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          前回請求金額
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          入金額
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          調整金額
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          繰越金額
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          今回請求金額 (税抜)
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          今回消費税額
        </th>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          今回請求金額 (税込)
        </th>
      </tr>
      <tr>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.prevInvAmount) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.payment) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.adjustment) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.carryoverNew) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.invWithoutTax) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.invTax) }}
        </td>
        <td style="font-size: 7.5pt; text-align: right; width: 70.7pt">
          {{ numToStrNum(pdfData.invShowAmount) }}
        </td>
      </tr>
    </table>
    <table v-if="isAmountTableComputed">
      <tr v-if="pdfData.invAmountTr10">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          10%対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxTr10) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxTr10) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountTr10) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountTr8Reduced">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          8%対象 (軽減税率 税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxTr8Reduced) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxTr8Reduced) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountTr8Reduced) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountTr8">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          8%対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxTr8) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxTr8) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountTr8) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountTr5">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          5%対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxTr5) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxTr5) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountTr5) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountTr0">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          0%対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxTr0) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxTr0) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountTr0) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountFree">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          非課税対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxFree) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxFree) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountFree) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountExemption">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          免税対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxExemption) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxExemption) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountExemption) }}
        </td>
      </tr>
      <tr v-if="pdfData.invAmountNon">
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          不課税対象 (税抜)
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invWithoutTaxNon) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          消費税額
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invTaxNon) }}
        </td>
        <th style="font-size: 7.5pt; width: 90pt; background-color: #cccccc">
          <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT"
            >合計金額 (税込)</span
          >
          <span v-else>請求金額 (税込)</span>
        </th>
        <td style="font-size: 7pt; text-align: right; width: 78pt">
          {{ numToStrNum(pdfData.invAmountNon) }}
        </td>
      </tr>
    </table>
    <table v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT">
      <tr>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          支払方法
        </th>
        <td style="font-size: 7.5pt; width: 87.6%">
          {{ paymentMethodTitle(pdfData.paymentMethod) }}
        </td>
      </tr>
      <tr>
        <th style="font-size: 7.5pt; width: 70.7pt; background-color: #cccccc">
          振込先
        </th>
        <td style="font-size: 7.5pt; width: 87.6%">
          <table style="font-size: 8pt" data-pdfmake='{"layout":"noBorders"}'>
            <tr v-for="item in pdfData.banks" :key="item.branchCode">
              <td style="width: 200pt">{{ bankCodeComputed(item) }}</td>
              <td>{{ item.depositorKana }}</td>
            </tr>
          </table>
        </td>
      </tr>
      <tr style="height: 80pt">
        <th
          style="
            font-size: 7.5pt;
            width: 70.7pt;
            margin-top: 35pt;
            background-color: #cccccc;
          "
        >
          備考
        </th>
        <td style="font-size: 7.5pt; width: 87.6%">
          {{ pdfData.remarks }}
        </td>
      </tr>
    </table>
    <div
      v-for="(item, index) in pdfData.details"
      :key="index"
      class="particular-page"
    >
      <div v-if="index === 0 || index % detailSizeComputed === 0">
        <table data-pdfmake='{"layout":"noBorders"}'>
          <tr class="pdf-pagebreak-before">
            <td style="font-size: 8pt; width: 250pt">
              <span v-if="pdfData.dataType === DataType.PURCHASESTATEMENT">
                送付元： {{ pdfData.publisher?.publisherCompanyNameOrg }}
              </span>
              <span v-else>
                請求元： {{ pdfData.publisher?.publisherCompanyNameOrg }}
              </span>
            </td>
            <td style="font-size: 8pt; text-align: right; width: 300pt">
              出力日：{{ outputDate }}
            </td>
          </tr>
        </table>
        <table style="font-size: 8pt" :style="detailStyleComputed">
          <tr>
            <th style="width: 38pt; background-color: #cccccc">明細日付</th>
            <th
              style="width: 125pt; background-color: #cccccc; margin-top: 6pt"
              rowspan="2"
            >
              明細項目
            </th>
            <th style="width: 52pt; background-color: #cccccc">単価</th>
            <th style="width: 52pt; background-color: #cccccc">数量</th>
            <th style="width: 40pt; background-color: #cccccc">単位</th>
            <th style="width: 60pt; background-color: #cccccc">金額</th>
            <th style="width: 60pt; background-color: #cccccc">消費税額</th>
            <th style="width: 60pt; background-color: #cccccc">請求金額</th>
          </tr>
          <tr>
            <th style="background-color: #cccccc">明細番号</th>
            <th style="background-color: #cccccc" colspan="3">部門</th>
            <th style="background-color: #cccccc" colspan="3">備考</th>
          </tr>
        </table>
        <table
          v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT"
          style="font-size: 8pt; border-collapse: collapse; margin: 0"
        >
          <th style="width: 270.5pt; background-color: #cccccc">メモ1</th>
          <th style="width: 270.5pt; background-color: #cccccc">メモ2</th>
        </table>
        <table
          v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT"
          style="font-size: 8pt; border-collapse: collapse; margin-top: 0"
        >
          <tr>
            <th style="width: 70.9pt; background-color: #cccccc">
              会計伝票日付
            </th>
            <th style="width: 70.9pt; background-color: #cccccc">
              借方負担部門
            </th>
            <th style="width: 70.9pt; background-color: #cccccc">借方科目</th>
            <th style="width: 70.9pt; background-color: #cccccc">
              借方補助科目
            </th>
            <th style="width: 70.9pt; background-color: #cccccc">
              貸方負担部門
            </th>
            <th style="width: 70.9pt; background-color: #cccccc">貸方科目</th>
            <th style="width: 70.9pt; background-color: #cccccc">
              貸方補助科目
            </th>
          </tr>
          <tr>
            <th style="background-color: #cccccc" colspan="7">摘要</th>
          </tr>
        </table>
      </div>
      <table style="font-size: 6pt" :style="detailStyleComputed">
        <tr>
          <td style="height: 12pt; width: 38pt; margin-top: 2pt">
            {{ formatDate(item.itemSlipDate) }}
          </td>
          <td style="height: 12pt; width: 125pt; margin-top: 8pt" rowspan="2">
            {{ item.itemProdCode }}<br />{{ item.itemName }}
          </td>
          <td
            style="
              height: 12pt;
              width: 52pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            {{ numToStrNum(item.itemPrice) }}
          </td>
          <td
            style="
              height: 12pt;
              width: 52pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            {{ numToStrNum(item.itemQty) }}
          </td>
          <td style="height: 12pt; width: 40pt; margin-top: 2pt">
            {{ item.itemUnit }}
          </td>
          <td style="height: 12pt; width: 60pt; text-align: right">
            {{ numToStrNum(item.itemWithoutTax) }}<br />
            <span v-if="item.taxType === TaxType.TAX" style="font-size: 5.5pt">
              (課税
              <span v-if="item.reducedTaxFlg === ReducedTaxFlg.REDUCED">
                軽減 </span
              >{{ item.taxRateSec }}%)
            </span>
            <span
              v-if="item.taxType === TaxType.TAXFREE"
              style="font-size: 5.5pt"
            >
              (非課税)
            </span>
            <span
              v-if="item.taxType === TaxType.TAXEXEMPTION"
              style="font-size: 5.5pt"
            >
              (免税)
            </span>
            <span
              v-if="item.taxType === TaxType.TAXNON"
              style="font-size: 5.5pt"
            >
              (不課税)
            </span>
          </td>
          <td
            v-if="pdfData.customer?.taxCorpId"
            style="
              height: 12pt;
              width: 60pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            -
          </td>
          <td
            v-if="pdfData.customer?.taxCorpId"
            style="
              height: 12pt;
              width: 60pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            -
          </td>
          <td
            v-if="!pdfData.customer?.taxCorpId"
            style="
              height: 12pt;
              width: 60pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            {{ item.itemTax }}
          </td>
          <td
            v-if="!pdfData.customer?.taxCorpId"
            style="
              height: 12pt;
              width: 60pt;
              text-align: right;
              margin-top: 2pt;
            "
          >
            {{ numToStrNum(item.itemAmount) }}
          </td>
        </tr>
        <tr>
          <td style="height: 12pt; margin-top: 2pt">
            {{ item.itemSlipNo }}
          </td>
          <td style="height: 12pt" colspan="3">
            {{ item.itemSecName }}
          </td>
          <td style="height: 12pt" colspan="3">
            {{ item.detailRemarks }}
          </td>
        </tr>
      </table>
      <table
        v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT"
        style="font-size: 6pt; border-collapse: collapse; margin: 0"
      >
        <td style="height: 12pt; width: 270.5pt">
          {{ item.itemFreeTxt1 }}
        </td>
        <td style="height: 12pt; width: 270.5pt">
          {{ item.itemFreeTxt2 }}
        </td>
      </table>
      <table
        v-if="pdfData.dataType !== DataType.PURCHASESTATEMENT"
        style="font-size: 6pt; border-collapse: collapse; margin-top: 0"
      >
        <tr>
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
          <td style="height: 12pt; width: 70.9pt" />
        </tr>
        <tr>
          <td style="height: 12pt" colspan="7" />
        </tr>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import pdfMake from 'pdfmake'
import htmlToPdfmake from 'html-to-pdfmake'

import { ref, computed, onMounted } from 'vue'
import {
  BanksInner,
  DataType,
  Preview,
  ReducedTaxFlg,
  TaxType,
} from '@/codegen'
import { formatDate, numToStrNum, paymentMethodTitle } from '@/plugins/utils'
import { JPY_CURRENCY, USD_CURRENCY } from '@/const/const'

interface PdfMakeNode {
  style: string[]
  stack: object
  nodeInfo: {
    startPosition: {
      pageNumber: number
    }
  }
}

interface GeneratePdfProps {
  pdfData: Preview
}

interface GeneratePdfEmits {
  (e: 'pdfData', pdfData: Blob): void
}

const props = defineProps<GeneratePdfProps>()
const emit = defineEmits<GeneratePdfEmits>()

const refPrintDom = ref()

const publisherAddressComputed = computed(() => {
  const publisher = props.pdfData.publisher
  return `${publisher?.publisherCountrySubentity ?? ''}${publisher?.publisherCityName ?? ''}${publisher?.publisherStreetName ?? ''}`
})
const customerAddressComputed = computed(() => {
  const customer = props.pdfData.customer
  return `${customer?.countrySubentity ?? ''}${customer?.cityName ?? ''}${customer?.streetName ?? ''}`
})

const isAmountTableComputed = computed(() => {
  if (
    props.pdfData.invAmountTr10 ||
    props.pdfData.invAmountTr8Reduced ||
    props.pdfData.invAmountTr8 ||
    props.pdfData.invAmountTr5 ||
    props.pdfData.invAmountTr0 ||
    props.pdfData.invAmountFree ||
    props.pdfData.invAmountNon ||
    props.pdfData.invAmountExemption
  )
    return true

  return false
})

const bankCodeComputed = computed(() => (bank: BanksInner) => {
  return (
    `${bank.fnclInstCode ? bank.fnclInstCode + ':' : ''}` +
    `${bank.branchCode ? bank.branchCode + ':' : ''}` +
    `${bank.depositSec ? bank.depositSec + ':' : ''}` +
    `${bank.accountNum ? bank.accountNum : ''}`
  )
})

const detailSizeComputed = computed(() => {
  return props.pdfData.dataType !== DataType.PURCHASESTATEMENT ? 7 : 16
})
const detailStyleComputed = computed(() => {
  return props.pdfData.dataType !== DataType.PURCHASESTATEMENT
    ? { borderCollapse: 'collapse', marginBottom: 0 }
    : {}
})

const outputDate = formatDate(new Date(), 'yyyy/MM/dd HH:mm')

onMounted(() => {
  // PDF変換元のHTMLを取得
  const reportContentForPdf = refPrintDom.value.outerHTML
  const option = {
    tableAutoSize: true,
    imagesByReference: true,
  }
  // HTMLからPdfmakeライブラリの形に変換
  const content = htmlToPdfmake(reportContentForPdf, option)

  pdfMake.fonts = {
    ipa: {
      normal: `${window.location.origin}/fonts/NotoSansJP-Regular.ttf`,
      bold: `${window.location.origin}/fonts/NotoSansJP-Bold.ttf`,
      italics: `${window.location.origin}/fonts/NotoSansJP-Regular.ttf`,
      bolditalics: `${window.location.origin}/fonts/NotoSansJP-Regular.ttf`,
    },
  }
  const defaultStyle = 'ipa'

  // PDF出力設定
  const documentDefined = {
    pageSize: 'A4',
    pageMargins: [20.25, 22.5, 20.25, 22.5],
    content: content.content,
    images: content.images,
    defaultStyle: {
      font: defaultStyle,
    },
    footer: (currentPage: number, pageCount: number) => {
      const footerFontSize = 8

      // 請求書明細情報のコンテンツデータ取得
      const detailsItems = content.content[0].stack
        .map((node: PdfMakeNode) => {
          return node.stack
        })
        .filter((stack: PdfMakeNode[]) => {
          if (stack !== undefined) {
            stack.filter((node: PdfMakeNode) => {
              return node.style && node.style.indexOf('particular-page')
            })
            return stack
          }
        })
        .flatMap((stack: PdfMakeNode[]) => {
          return stack[0]
        })

      // 明細情報が存在するページに注釈テキスト渡す
      let annotationText = ''
      detailsItems.forEach((node: PdfMakeNode) => {
        if (node.nodeInfo?.startPosition.pageNumber === currentPage) {
          annotationText = '※商品コードは16桁まで表示されます。'
          return
        }
      })
      return [
        {
          layout: 'noBorders',
          table: {
            widths: ['*', '*', '*'],
            body: [
              [
                {
                  fontSize: footerFontSize,
                  text: annotationText,
                  margin: [20.25, 0, 0, 0],
                },
                {
                  fontSize: footerFontSize,
                  text: currentPage.toString() + ' / ' + pageCount,
                  alignment: 'center',
                },
                '',
              ],
            ],
          },
        },
      ]
    },
    pageBreakBefore: (currentNode: PdfMakeNode) => {
      return (
        currentNode.style &&
        currentNode.style.indexOf('pdf-pagebreak-before') > -1
      )
    },
  }

  // PDFデータ作成
  pdfMake.createPdf(documentDefined).getBlob((blob: Blob) => {
    emit('pdfData', blob)
  })
})
</script>
