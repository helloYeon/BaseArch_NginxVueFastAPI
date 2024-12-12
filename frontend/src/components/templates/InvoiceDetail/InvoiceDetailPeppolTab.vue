<template>
  <InvoiceDetailPeppolTabCommonContent title="請求情報">
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書番号</p>
        <p>{{ peppol.iBT001 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書発行日</p>
        <p>{{ peppol.iBT002 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">請求書発行時刻</p>
        <p>{{ peppol.iBT168 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書タイプコード</p>
        <p>{{ peppol.iBT003 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書通貨コード</p>
        <p>{{ peppol.iBT005 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">税会計報告用通貨コード</p>
        <p>{{ peppol.iBT006 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">課税基準日</p>
        <p>{{ peppol.iBT007 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">課税基準日コード</p>
        <p>{{ peppol.iBG14?.iBT008 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">支払期日</p>
        <p>{{ peppol.iBT009 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">買い手参照</p>
        <p>{{ peppol.iBT010 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求期間開始日</p>
        <p>{{ peppol.iBG14?.iBT073 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">請求期間終了日</p>
        <p>{{ peppol.iBG14?.iBT074 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">プロジェクト参照</p>
        <p>{{ peppol.aUTO12?.iBT011 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">契約書参照</p>
        <p>{{ peppol.aUTO7?.iBT012 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">購買発注参照</p>
        <p>{{ peppol.aUTO2?.iBT013 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">受注参照</p>
        <p>{{ peppol.aUTO2?.iBT014 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">受取通知書参照</p>
        <p>{{ peppol.aUTO5?.iBT015 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">出荷案内書参照</p>
        <p>{{ peppol.aUTO4?.iBT016 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">入札又はロット参照</p>
        <p>{{ peppol.aUTO6?.iBT017 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求するオブジェクトID</p>
        <p>{{ peppol.aUTO8?.iBT018?.value }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">請求するオブジェクトIDのスキーマID</p>
        <p>{{ peppol.aUTO8?.iBT018?.schemeID }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">買い手会計参照</p>
        <p>{{ peppol.iBT019 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書注釈内容</p>
        <p>{{ peppol.iBT022 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">
          プロセスコントロールビジネスプロセスタイプ
        </p>
        <p>{{ peppol.iBT024 }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">プロセスコントロール仕様ID</p>
        <p>{{ peppol.iBT023 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3" />
      <v-col class="pa-0 ma-3" />
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="支払い条件">
    <v-table class="table" density="compact">
      <thead class="table-header">
        <tr>
          <th />
          <th class="font-weight-bold text-center">支払条件指示ID</th>
          <th class="font-weight-bold text-center">支払条件</th>
          <th class="font-weight-bold text-center">支払条件金額</th>
          <th class="font-weight-bold text-center">分割支払期日</th>
        </tr>
      </thead>
      <CommonEmptyTableRow v-if="!peppol.iBG33" :columns="5" />
      <tbody v-for="(item, index) in peppol.iBG33" :key="index">
        <tr>
          <td class="font-weight-bold text-center index">
            {{ index + 1 }}
          </td>
          <td class="text-right">{{ item.iBT187 }}</td>
          <td>{{ item.iBT020 }}</td>
          <td class="text-right">
            {{ strNumToLocaleStringNum(item.iBT176?.value) }}
          </td>
          <td class="text-right">
            {{ item.iBT177 }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="先行請求書への参照">
    <v-row
      v-for="item in peppol.iBG03"
      :key="item.aUTO3?.iBT025"
      class="row row-border"
    >
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">先行請求書への参照</p>
        <p>{{ item.aUTO3?.iBT025 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">先行請求書発行日</p>
        <p>{{ item.aUTO3?.iBT026 }}</p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="添付書類">
    <v-table class="table" density="compact">
      <thead class="table-header">
        <tr>
          <th />
          <th class="font-weight-bold text-center">添付書類への参照</th>
          <th class="font-weight-bold text-center">添付書類の説明</th>
          <th class="font-weight-bold text-center">外部ドキュメントの場所</th>
          <th class="font-weight-bold text-center">添付書類</th>
          <th class="font-weight-bold text-center">添付書類MIMEコード</th>
          <th class="font-weight-bold text-center">添付書類ファイル名</th>
        </tr>
      </thead>
      <CommonEmptyTableRow v-if="!peppol.iBG24" :columns="7" />
      <tbody v-for="(item, index) in peppol.iBG24" :key="index">
        <tr>
          <td class="font-weight-bold text-center index">
            {{ index + 1 }}
          </td>
          <td>{{ item.iBT122 }}</td>
          <td>{{ item.iBT123 }}</td>
          <td>
            {{ item.aUTO10?.aUTO11?.iBT124 }}
          </td>
          <td>{{ item.aUTO10?.iBT125?.value }}</td>
          <td>{{ item.aUTO10?.iBT125?.mimeCode }}</td>
          <td>{{ item.aUTO10?.iBT125?.filename }}</td>
        </tr>
      </tbody>
    </v-table>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="売り手(販売者)情報">
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">名称</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO25?.iBT027 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">商号</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO17?.iBT028 }}</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">売り手（販売者）ID</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">ID</th>
              <th class="font-weight-bold text-center">スキーマID</th>
            </tr>
          </thead>
          <CommonEmptyTableRow
            v-if="!peppol.iBG04.aUTO13?.aUTO14"
            :columns="3"
          />
          <tbody
            v-for="(item, index) in peppol.iBG04.aUTO13?.aUTO14"
            :key="index"
          >
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td class="text-right">
                {{ item.iBT029?.value }}
              </td>
              <td class="text-right">
                {{ item.iBT029?.schemeID }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
      <v-divider :thickness="2" color="black" />
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">法人ID</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO25?.iBT030?.value }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">法人ID スキーマID</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO25?.iBT030?.schemeID }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">税ID</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO20?.iBT031 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">税スキーマID</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO20?.aUTO21?.iBT0311 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">税登録ID</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO22?.iBT032 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">追加法的情報</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO25?.iBT033 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">電子アドレス</p>
        <p>{{ peppol.iBG04.aUTO13?.iBT034?.value }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">電子アドレス スキーマID</p>
        <p>{{ peppol.iBG04.aUTO13?.iBT034?.schemeID }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">銀行が採番した債権者の識別子</p>
        <p>{{ peppol.iBG04.aUTO13?.aUTO15?.iBT090?.value }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄1</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.iBT035 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄2</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.iBT036 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所欄3</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.aUTO18?.iBT162 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所 市区町村</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.iBT037 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">郵便番号</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.iBT038 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所 都道府県</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.iBT039 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">国コード</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG05?.aUTO19?.iBT040 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">連絡先</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG06?.iBT041 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">連絡先電話番号</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG06?.iBT042 }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">連絡先電子メールアドレス</p>
        <p>{{ peppol.iBG04.aUTO13?.iBG06?.iBT043 }}</p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="買い手(購入者)情報">
    <v-row class="row row-border">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">名称</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO33?.iBT044 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">商号</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO28?.iBT045 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">ID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO27?.iBT046?.value }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">ID スキーマID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO27?.iBT046?.schemeID }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">法人ID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO33?.iBT047?.value }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">法人ID スキーマID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO33?.iBT047?.schemeID }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">税ID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO31?.iBT048 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">税ID スキーマID</p>
        <p>{{ peppol.iBG07.aUTO26?.aUTO31?.aUTO32?.iBT0481 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">電子アドレス</p>
        <p>{{ peppol.iBG07.aUTO26?.iBT049?.value }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">電子アドレス スキーマID</p>
        <p>{{ peppol.iBG07.aUTO26?.iBT049?.schemeID }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄1</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.iBT050 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄2</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.iBT051 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所欄3</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.aUTO29?.iBT163 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所 市区町村</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.iBT052 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">郵便番号</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.iBT053 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所 都道府県</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.iBT054 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">国コード</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG08?.aUTO30?.iBT055 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">連絡先</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG09?.iBT056 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">連絡先電話番号</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG09?.iBT057 }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">連絡先電子メールアドレス</p>
        <p>{{ peppol.iBG07.aUTO26?.iBG09?.iBT058 }}</p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="支払先">
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">支払先名称</p>
        <p>{{ peppol.iBG10?.aUTO35?.iBT059 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">支払先ID</p>
        <p>{{ peppol.iBG10?.aUTO34?.iBT060?.value }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">支払先ID スキーマID</p>
        <p>{{ peppol.iBG10?.aUTO34?.iBT060?.schemeID }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">支払先登録企業ID</p>
        <p>{{ peppol.iBG10?.aUTO36?.iBT061?.value }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">支払先登録企業ID スキーマID</p>
        <p>{{ peppol.iBG10?.aUTO36?.iBT061?.schemeID }}</p>
      </v-col>
      <v-col class="pa-0 ma-3" />
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="売り手税務代理人">
    <v-row class="row row-border">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">名称</p>
        <p>{{ peppol.iBG11?.aUTO37?.iBT062 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">税ID</p>
        <p>{{ peppol.iBG11?.aUTO40?.iBT063 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">税スキーマID</p>
        <p>{{ peppol.iBG11?.aUTO40?.aUTO41?.iBT0631 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3" />
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄1</p>
        <p>{{ peppol.iBG11?.iBG12?.iBT064 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄2</p>
        <p>{{ peppol.iBG11?.iBG12?.iBT065 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所欄3</p>
        <p>{{ peppol.iBG11?.iBG12?.aUTO38?.iBT164 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所 市区町村</p>
        <p>{{ peppol.iBG11?.iBG12?.iBT066 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">郵便番号</p>
        <p>{{ peppol.iBG11?.iBG12?.iBT067 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所 都道府県</p>
        <p>{{ peppol.iBG11?.iBG12?.iBT068 }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">国コード</p>
        <p>{{ peppol.iBG11?.iBG12?.aUTO39?.iBT069 }}</p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="納入先">
    <v-row class="row row-border">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">名称</p>
        <p>{{ peppol.iBG13?.aUTO45?.aUTO46?.iBT070 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">ID</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBT071?.value }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">納入先ID 税スキーマID</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBT071?.schemeID }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">実際納入日</p>
        <p>{{ peppol.iBG13?.iBT072 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄1</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.iBT075 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所欄2</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.iBT076 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所欄3</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.aUTO43?.iBT165 }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">住所 市区町村</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.iBT077 }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">郵便番号</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.iBT078 }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">住所 都道府県</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.iBT079 }}</p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">国コード</p>
        <p>{{ peppol.iBG13?.aUTO42?.iBG15?.aUTO44?.iBT080 }}</p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="支払い指示">
    <v-expansion-panels v-model="panel" multiple selected-class=".selected">
      <v-expansion-panel
        v-for="(item, index) in peppol.iBG16"
        :key="index"
        class="mt-8"
      >
        <v-expansion-panel-title
          color="#f6f6f6"
          expand-icon="mdi-plus"
          collapse-icon="mdi-minus"
          class="panel-title"
        >
          <p class="panel-title__text">{{ index + 1 }}件目</p>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row class="row row-border">
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">支払指示ID</p>
              <p>{{ item.iBT178 }}</p>
            </v-col>
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">支払手段タイプコード</p>
              <p>{{ item.iBT081?.value }}</p>
            </v-col>
            <v-col class="pa-0 ma-3" />
          </v-row>
          <v-row class="row row-border">
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">支払手段内容説明</p>
              <p>{{ item.iBT081?.name }}</p>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <p class="font-weight-bold tab-sub-title mb-3">送金情報</p>
              <v-table class="table" density="compact">
                <thead class="table-header">
                  <tr>
                    <th />
                    <th class="font-weight-bold text-center">送金情報</th>
                    <th class="font-weight-bold text-center">
                      送金情報 スキーマID
                    </th>
                  </tr>
                </thead>
                <CommonEmptyTableRow v-if="!item.iBT083" :columns="3" />
                <tbody
                  v-for="(info, infoIndex) in item.iBT083"
                  :key="infoIndex"
                >
                  <tr>
                    <td class="font-weight-bold text-center index">
                      {{ infoIndex + 1 }}
                    </td>
                    <td>
                      {{ info.value }}
                    </td>
                    <td class="text-right">
                      {{ info.schemeID }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-divider :thickness="2" color="black" />
          </v-row>
          <v-row class="row row-border">
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">支払先口座ID</p>
              <p>{{ item.iBG17?.iBT084?.value }}</p>
            </v-col>
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">支払先口座ID スキーマID</p>
              <p>{{ item.iBG17?.iBT084?.schemeID }}</p>
            </v-col>
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">支払先口座名義人名</p>
              <p>{{ item.iBG17?.iBT085 }}</p>
            </v-col>
          </v-row>
          <v-row class="row row-border">
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">支払先金融機関ID</p>
              <p>{{ item.iBG17?.aUTO48?.iBT086 }}</p>
            </v-col>
          </v-row>
          <v-row class="row row-border">
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">住所欄1</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.iBT169 }}</p>
            </v-col>
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">住所欄2</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.iBT170 }}</p>
            </v-col>
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">住所欄3</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.aUTO49?.iBT174 }}</p>
            </v-col>
          </v-row>
          <v-row class="row row-border">
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">住所 市区町村</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.iBT171 }}</p>
            </v-col>
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">郵便番号</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.iBT172 }}</p>
            </v-col>
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">住所 都道府県</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.iBT173 }}</p>
            </v-col>
          </v-row>
          <v-row class="row row-border">
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">国コード</p>
              <p>{{ item.iBG17?.aUTO48?.iBG34?.aUTO50?.iBT175 }}</p>
            </v-col>
          </v-row>
          <v-row class="row row-border">
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">支払カード番号</p>
              <p>{{ item.iBG18?.iBT087 }}</p>
            </v-col>
            <v-col class="col-border pa-0 ma-3">
              <p class="font-weight-bold">カード名義人氏名</p>
              <p>{{ item.iBG18?.iBT088 }}</p>
            </v-col>
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">マンデーション参照ID</p>
              <p>{{ item.iBG19?.iBT089 }}</p>
            </v-col>
          </v-row>
          <v-row class="row">
            <v-col class="pa-0 ma-3">
              <p class="font-weight-bold">自動引落口座ID</p>
              <p>{{ item.iBG19?.aUTO51?.iBT091 }}</p>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="支払い内容">
    <v-row>
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">支払済金額</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">支払ID</th>
              <th class="font-weight-bold text-center">支払済金額</th>
              <th class="font-weight-bold text-center">
                支払済金額が請求書に差引記載される日
              </th>
              <th class="font-weight-bold text-center">支払タイプ</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!peppol.iBG35" :columns="5" />
          <tbody v-for="(item, index) in peppol.iBG35" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td class="text-right">
                {{ item.iBT179 }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT180?.value) }}
              </td>
              <td class="text-right">
                {{ item.iBT181 }}
              </td>
              <td>
                {{ item.iBT182 }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
      <v-divider :thickness="2" color="black" />
    </v-row>
    <v-row>
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">請求書レベルの返金</p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金金額(税抜)
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの返金<br />金額の基準となる金額
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金の率
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金の理由
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金の理由コード
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金の課税分類コード
              </th>
              <th class="font-weight-bold text-center">税スキーマ</th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />返金の税率
              </th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!peppol.iBG20" :columns="9" />
          <tbody v-for="(item, index) in peppol.iBG20" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT092?.value) }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT093?.value) }}
              </td>
              <td class="text-right">
                {{ item.iBT094 }}
              </td>
              <td>
                {{ item.iBT097 }}
              </td>
              <td>
                {{ item.iBT098 }}
              </td>
              <td>
                {{ item.aUTO57?.iBT095 }}
              </td>
              <td>
                {{ item.aUTO57?.aUTO58?.iBT0951 }}
              </td>
              <td class="text-right">
                {{ item.aUTO57?.iBT096 }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
      <v-divider :thickness="2" color="black" />
    </v-row>
    <v-row>
      <v-col>
        <p class="font-weight-bold tab-sub-title mb-3">
          請求書レベルの追加請求
        </p>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求金額(税抜)
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの追加請求<br />金額の基準となる金額
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求の率
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求の理由
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求の理由コード
              </th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求の課税分類コード
              </th>
              <th class="font-weight-bold text-center">税スキーマ</th>
              <th class="font-weight-bold text-center">
                請求書レベルの<br />追加請求の税率
              </th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!peppol.iBG21" :columns="5" />
          <tbody v-for="(item, index) in peppol.iBG21" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT099?.value) }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT100?.value) }}
              </td>
              <td class="text-right">
                {{ item.iBT101 }}
              </td>
              <td>
                {{ item.iBT104 }}
              </td>
              <td>
                {{ item.iBT105 }}
              </td>
              <td>
                {{ item.aUTO62?.iBT102 }}
              </td>
              <td>
                {{ item.aUTO62?.aUTO63?.iBT1021 }}
              </td>
              <td class="text-right">
                {{ item.aUTO62?.iBT103 }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
      <v-divider :thickness="2" color="black" />
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">値引後請求書明細行金額の合計</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT106?.value) }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書レベルの返金の合計</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT107?.value) }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">請求書レベルの追加請求の合計</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT108?.value) }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書合計金額(税抜)</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT109?.value) }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">請求書合計金額(税込)</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT112?.value) }}</p>
      </v-col>
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">支払済金額</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT113?.value) }}</p>
      </v-col>
    </v-row>
    <v-row class="row row-border">
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">丸めるための金額</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT114?.value) }}</p>
      </v-col>
      <v-col class="col-border pa-0 ma-3">
        <p class="font-weight-bold">差引請求金額</p>
        <p>{{ strNumToLocaleStringNum(peppol.iBG22?.iBT115?.value) }}</p>
      </v-col>
      <v-col class="pa-0 ma-3" />
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="税内訳情報">
    <v-row>
      <v-col>
        <v-table class="table" density="compact">
          <thead class="table-header">
            <tr>
              <th />
              <th class="font-weight-bold text-center">課税分類コード</th>
              <th class="font-weight-bold text-center">
                課税分類コード スキーマID
              </th>
              <th class="font-weight-bold text-center">課税分類毎の税率</th>
              <th class="font-weight-bold text-center">
                課税分類毎の課税基準額
              </th>
              <th class="font-weight-bold text-center">課税分類毎の消費税額</th>
            </tr>
          </thead>
          <CommonEmptyTableRow v-if="!peppol.aUTO64.iBG23" :columns="6" />
          <tbody v-for="(item, index) in peppol.aUTO64.iBG23" :key="index">
            <tr>
              <td class="font-weight-bold text-center index">
                {{ index + 1 }}
              </td>
              <td>
                {{ item.aUTO68?.iBT118 }}
              </td>
              <td>
                {{ item.aUTO68?.aUTO69?.iBT1181 }}
              </td>
              <td class="text-right">
                {{ item.aUTO68?.iBT119 }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT116?.value) }}
              </td>
              <td class="text-right">
                {{ strNumToLocaleStringNum(item.iBT117?.value) }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">請求書消費税合計金額</p>
        <p>
          {{ strNumToLocaleStringNum(peppol.aUTO64?.iBT110?.value) }}
        </p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="会計通貨での税内訳情報">
    <v-row
      v-for="item in peppol.iBG37?.iBG38"
      :key="item.iBT190?.value"
      class="row row-border"
    >
      <v-col class="col-border pa-0 pr-8 ma-3">
        <p class="font-weight-bold">会計通貨での課税分類コード</p>
        <p>{{ item.aUTO72?.iBT192 }}</p>
      </v-col>
      <v-col class="col-border pa-0 pr-8 ma-3">
        <p class="font-weight-bold">会計通貨での課税分類毎の税率</p>
        <p>{{ item.aUTO72?.iBT193 }}</p>
      </v-col>
      <v-col class="pa-0 pr-8 ma-3">
        <p class="font-weight-bold">会計通貨での課税分類毎の消費税額</p>
        <p>
          {{ strNumToLocaleStringNum(item.iBT190?.value) }}
        </p>
      </v-col>
    </v-row>
    <v-row class="row">
      <v-col class="pa-0 ma-3">
        <p class="font-weight-bold">会計通貨での請求書消費税合計金額</p>
        <p>
          {{ strNumToLocaleStringNum(peppol.iBG37?.iBT111?.value) }}
        </p>
      </v-col>
    </v-row>
  </InvoiceDetailPeppolTabCommonContent>
  <InvoiceDetailPeppolTabCommonContent title="請求書明細行">
    <v-table class="table" density="compact">
      <thead class="table-header">
        <tr>
          <th rowspan="2" />
          <th class="font-weight-bold text-center" rowspan="2">
            請求書<br />明細行ID
          </th>
          <th class="font-weight-bold text-center" rowspan="2">
            明細行<br />文書ID
          </th>
          <th class="font-weight-bold text-center" rowspan="2">品名</th>
          <th class="font-weight-bold text-center" rowspan="2">
            請求書明細行の<br />期間開始日
          </th>
          <th class="font-weight-bold text-center" colspan="2">品目単価</th>
          <th class="font-weight-bold text-center" rowspan="2">
            品目単価<br />(値引後/税抜)
          </th>
          <th class="font-weight-bold text-center" rowspan="2">
            値引後請求書<br />明細行金額(税抜)
          </th>
          <th class="font-weight-bold text-center" rowspan="2">操作</th>
        </tr>
        <tr>
          <th class="font-weight-bold text-center">基準数量</th>
          <th class="font-weight-bold text-center">単位コード</th>
        </tr>
      </thead>
      <CommonEmptyTableRow
        v-if="!peppol.invoiceLineInPeppolDetail"
        :columns="10"
      />
      <tbody
        v-for="(item, index) in peppol.invoiceLineInPeppolDetail"
        :key="index"
      >
        <tr>
          <td class="font-weight-bold text-center index">
            {{ index + 1 }}
          </td>
          <td class="text-right">
            {{ item.iBT126 }}
          </td>
          <td class="text-right">
            {{ item.iBG36?.iBT188 }}
          </td>
          <td>{{ item.iBG31.iBT153 }}</td>
          <td class="text-right">
            {{ item.iBG26?.iBT134 }}
          </td>
          <td class="text-right">
            {{ item.iBG29.iBT149?.value }}
          </td>
          <td>
            {{ item.iBG29.iBT149?.unitCode }}
          </td>
          <td class="text-right">
            {{ strNumToLocaleStringNum(item.iBG29?.iBT146?.value) }}
          </td>
          <td class="text-right">
            {{ strNumToLocaleStringNum(item.iBT131.value) }}
          </td>
          <td
            class="d-flex justify-center align-center dialog"
            @click="emit('openDialog', item.id)"
          >
            <v-icon icon="mdi-plus-box-outline" />
            <p class="dialog__text ml-1">詳細</p>
          </td>
        </tr>
      </tbody>
    </v-table>
  </InvoiceDetailPeppolTabCommonContent>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import InvoiceDetailPeppolTabCommonContent from '@/components/templates/InvoiceDetail/InvoiceDetailPeppolTabCommonContent.vue'
import CommonEmptyTableRow from '@/components/templates/Common/CommonEmptyTableRow.vue'
import { Peppol } from '@/codegen'
import { strNumToLocaleStringNum } from '@/plugins/utils'

interface PeppolProps {
  peppol: Peppol
}

interface PeppolEmits {
  (e: 'openDialog', id: number): void
}

const props = defineProps<PeppolProps>()
const emit = defineEmits<PeppolEmits>()

const panel = ref(props.peppol.iBG16?.map((_, i: number) => i))
</script>

<style lang="scss" scoped>
p {
  font-size: 12px;
  color: #222222;
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

  & .dialog {
    color: #b11048;
    cursor: pointer;
    &__text {
      color: #b11048;
    }
  }
}

.panel-title {
  font-size: 1.3rem;
  font-weight: bold;
  &__text {
    color: #222222;
  }
}
.v-expansion-panel-title--active {
  :deep(.v-expansion-panel-title__overlay) {
    opacity: 0;
  }
}
</style>
