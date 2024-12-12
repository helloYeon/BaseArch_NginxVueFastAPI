<template>
  <div v-show="settingsStore.mode === SettingsMode.CSV">
    <SettingsCsv
      v-model:invoice-detail="invoiceDetail"
      v-model:particulars="particulars"
      v-model:common="common"
      v-model:csv-download-type="csvDownloadType"
    />
  </div>
  <div v-show="settingsStore.mode === SettingsMode.AUTH">
    <SettingsAuth
      v-model:access-allow-users="accessAllowUsers"
      v-model:access-deny-users="accessDenyUsers"
      @allow-user-list-sort="sortActionAllowUserList"
      @denny-user-list-sort="sortActionDennyUserList"
    />
  </div>
  <div v-show="settingsStore.mode === SettingsMode.PAYMENT_CODE">
    <SettingsPaymentCode
      v-model:payment-code-list="paymentCodeList"
      v-model:selected-company-infos-id="selectedCompanyInfosIdComputed"
      :company-integrations="companyIntegrations"
      @change-company="changeCompany"
      @payment-code-list-sort="sortActionPaymentCode"
    />
  </div>
  <div v-show="settingsStore.mode === SettingsMode.COMPANY_INFOS">
    <SettingCompanyInfos :company-infos="companyInfos" />
  </div>
  <CommonFixedFooter
    :is-hidden-cancel-button="isHiddenCancelButton"
    @cancel-event="cancelEvent"
    @save-event="saveEvent"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  ItemsApi,
  OutputsItem,
  PutInvoiceOutputsItemsRequest,
  AccessApi,
  IsDeny,
  UserAccessItem,
  PostAdminAccessRequest,
  MstType,
  IntegrationApi,
  CompanyIntegrationsItem,
  SettingApi,
  PutSettingPaymentCodeRequest,
  PaymentCodeData,
  TestsApi,
  GetCompanyInfos200ResponsePayloadInner,
  PutCompanyInfosOperationRequest,
  MeApi,
  PatchUserMeStatusRequest,
  CsvDownloadType,
  PatchUserMeStatus,
} from '@/codegen'
import { ClientConfig } from '@/plugins/apiClient'
import { useApiProgressStore } from '@/store/apiProgress'
import { useSettingsStore, SettingsMode } from '@/store/settings'
import SettingsCsv from '@/components/templates/Settings/SettingsCsv/SettingsCsv.vue'
import SettingsAuth from '@/components/templates/Settings/SettingsAuth/SettingsAuth.vue'
import SettingsPaymentCode from '@/components/templates/Settings/SettingsPaymentCode/SettingsPaymentCode.vue'
import SettingCompanyInfos from '@/components/templates/Settings/SettingCompanyInfos/SettingCompanyInfos.vue'
import CommonFixedFooter from '@/components/templates/Common/CommonFixedFooter.vue'
import { usePaymentCodeStore } from '@/store/paymentCode'
import { useAuthUserStore } from '@/store/authUser'
import { useLoadingStore } from '@/store/loading'
import { isStaging, isProduction } from '@/utils'

export interface SettingListInterface extends OutputsItem {
  child: SettingListInterface[]
  indeterminate: boolean
}

const apiProgressStore = useApiProgressStore()
const settingsStore = useSettingsStore()
const paymentCodeStore = usePaymentCodeStore()
const authUserStore = useAuthUserStore()
const loadingStore = useLoadingStore()

const itemApi = new ItemsApi(new ClientConfig())
const accessApi = new AccessApi(new ClientConfig())
const integrationApi = new IntegrationApi(new ClientConfig())
const settingApi = new SettingApi(new ClientConfig())
const testsApi = new TestsApi(new ClientConfig())
const meApi = new MeApi(new ClientConfig())

const invoiceDetail = ref<SettingListInterface[]>([])
const particulars = ref<SettingListInterface[]>([])
const common = ref<SettingListInterface[]>([])

const accessAllowUsers = ref<UserAccessItem[]>([])
const accessDenyUsers = ref<UserAccessItem[]>([])

const companyIntegrations = ref<CompanyIntegrationsItem[]>([])
const paymentCodeList = ref<PaymentCodeData[]>([])

const companyInfos = ref<GetCompanyInfos200ResponsePayloadInner[]>([])

const csvDownloadType = ref<CsvDownloadType>(CsvDownloadType.ALLITEMS)

const selectedCompanyInfosIdComputed = computed({
  get: () => paymentCodeStore.companyInfosId ?? 0,
  set: (value) => (paymentCodeStore.companyInfosId = value),
})

const isHiddenCancelButton = computed(() => {
  return (
    settingsStore.mode === SettingsMode.CSV &&
    csvDownloadType.value === CsvDownloadType.CREATINGYOUROWNINVOICE
  )
})

// apiResponseを画面表示用に整形
// @return SettingListInterface[]
const csvDataShapingToSetting = (data: OutputsItem[], type: MstType) => {
  const list: SettingListInterface[] = data
    .filter(({ mstType }) => mstType === type)
    .sort((first, second) => first.userSortOrder - second.userSortOrder)
    .map((item) => {
      return { ...item, child: [], indeterminate: false }
    })

  list.reverse().forEach((item) => {
    const parentIndex = list.findIndex(
      ({ mstSortOrder }) => mstSortOrder === item.mstParentSortOrder
    )
    if (list[parentIndex]) {
      list[parentIndex].child.unshift(item)
    }
  })

  return list
    .reverse()
    .filter(({ mstParentSortOrder }) => mstParentSortOrder === 0)
}

// apiRequest用に整形
// @return OutputsItem[]
const csvDataShapingToApi = (data: SettingListInterface[]): OutputsItem[] => {
  const request: OutputsItem[] = []

  // childの中身を展開
  // 再帰的に実行
  const openChild = (item: SettingListInterface[]) => {
    item.forEach((element) => {
      const item = { ...element, child: undefined, indeterminate: undefined }
      delete item.child
      delete item.indeterminate
      request.push(item)
      if (element.child.length) openChild(element.child)
    })
  }
  openChild(data)

  // sort再設定
  return request.map((item, index) => {
    return { ...item, userSortOrder: index + 1 }
  })
}

// 出力項目取得
const getCsvSettingMaster = async () => {
  invoiceDetail.value = []
  particulars.value = []
  common.value = []

  const response = await itemApi.getInvoiceOutputsItems()

  invoiceDetail.value = csvDataShapingToSetting(
    response.payload,
    MstType.INVOICES
  )
  particulars.value = csvDataShapingToSetting(
    response.payload,
    MstType.PARTICULARS
  )
  common.value = csvDataShapingToSetting(response.payload, MstType.COMMON)
}

// Csv出力項目を設定前に戻す
const cancelCsvSetting = async () => {
  apiProgressStore.cancelSetting = true
  await getCsvSettingMaster()
  apiProgressStore.cancelSetting = false
}

// Csv出力項目更新
const updateCsvSetting = async () => {
  if (!invoiceDetail.value || !particulars.value || !common.value) return

  apiProgressStore.saveSetting = true

  const requestBody: PutInvoiceOutputsItemsRequest = {
    putInvoiceOutputsItems: {
      data: csvDataShapingToApi(invoiceDetail.value)
        .concat(csvDataShapingToApi(particulars.value))
        .concat(csvDataShapingToApi(common.value)),
    },
  }

  await itemApi.putInvoiceOutputsItems(requestBody)

  apiProgressStore.saveSetting = false
}

// 権限設定項目取得
const getAuthControl = async () => {
  const response = await accessApi.getAdminAccess()

  accessAllowUsers.value = response.payload.filter(
    ({ isDeny }) => isDeny === IsDeny.IS_ALLOW
  )
  accessDenyUsers.value = response.payload.filter(
    ({ isDeny }) => isDeny === IsDeny.IS_DENY
  )
  // ソート実行
  sortActionAllowUserList()
  sortActionDennyUserList()
}

// 権限項目を設定前に戻す
const cancelAuthSetting = async () => {
  apiProgressStore.cancelSetting = true
  await getAuthControl()
  apiProgressStore.cancelSetting = false
}

// 権限項目更新
const updateAuthSetting = async () => {
  apiProgressStore.saveSetting = true
  const requestBody: PostAdminAccessRequest = {
    postAdminAccess: {
      data: accessAllowUsers.value.concat(accessDenyUsers.value),
    },
  }
  await accessApi.postAdminAccess(requestBody)
  apiProgressStore.saveSetting = false
}

// 利用可能ユーザーソート実行
const sortActionAllowUserList = () => {
  accessAllowUsers.value.sort((f, s) => {
    const fValue = f.lastName + f.firstName
    const sValue = s.lastName + s.firstName
    if (fValue === sValue) return 0
    if (authUserStore.allowUserListSortOrder) {
      return fValue > sValue ? -1 : 1
    } else {
      return fValue < sValue ? -1 : 1
    }
  })
}
// 利用可能ユーザーソート実行
const sortActionDennyUserList = () => {
  accessDenyUsers.value.sort((f, s) => {
    const fValue = f.lastName + f.firstName
    const sValue = s.lastName + s.firstName
    if (fValue === sValue) return 0
    if (authUserStore.denyUserListSortOrder) {
      return fValue > sValue ? -1 : 1
    } else {
      return fValue < sValue ? -1 : 1
    }
  })
}

// 統合企業情報取得
const getCompanyIntegrations = async () => {
  const response = await integrationApi.getCompanyIntegrations()
  companyIntegrations.value = response.payload
}

// 支払先コード取得
const getPaymentCode = async () => {
  const response = await settingApi.getSettingPaymentCode({
    companyInfosId: selectedCompanyInfosIdComputed.value,
  })
  paymentCodeList.value = response.payload.items
  selectedCompanyInfosIdComputed.value = response.payload.companyInfosId
  // ソート実行
  sortActionPaymentCode()
}

// 支払先コード更新
const updatePaymentCodeSetting = async () => {
  if (!selectedCompanyInfosIdComputed.value) return

  apiProgressStore.saveSetting = true

  const requestBody: PutSettingPaymentCodeRequest = {
    putPaymentCode: {
      items: paymentCodeList.value,
      companyInfosId: selectedCompanyInfosIdComputed.value,
    },
  }

  await settingApi.putSettingPaymentCode(requestBody)

  apiProgressStore.saveSetting = false
}

// 支払先コードを設定前に戻す
const cancelPaymentCodeSetting = async () => {
  apiProgressStore.cancelSetting = true
  await getPaymentCode()
  apiProgressStore.cancelSetting = false
}

// 支払先コードソート実行
const sortActionPaymentCode = () => {
  const sort = paymentCodeStore.sort
  paymentCodeList.value = paymentCodeList.value.sort((f, s) => {
    const fValue = f[sort]
    const sValue = s[sort]
    if (fValue === sValue) return 0
    if (paymentCodeStore.sortOrder) {
      return fValue > sValue ? -1 : 1
    } else {
      return fValue < sValue ? -1 : 1
    }
  })
}

// 企業変更
const changeCompany = async () => {
  if (!selectedCompanyInfosIdComputed.value) return

  apiProgressStore.cancelSetting = true
  await getPaymentCode()
  apiProgressStore.cancelSetting = false
}

// 企業情報一覧取得
const getCompanyInfos = async () => {
  // テスト用のため開発環境でのみ実行する
  if (isProduction() || isStaging()) return

  const response = await testsApi.getCompanyInfos()
  companyInfos.value = response.payload
}

// 企業情報一覧を更新
const updateCompanyInfosSetting = async () => {
  // テスト用のため開発環境でのみ実行する
  if (isProduction() || isStaging()) return

  apiProgressStore.saveSetting = true

  const requestBody: PutCompanyInfosOperationRequest = {
    putCompanyInfosRequest: {
      data: companyInfos.value,
    },
  }

  await testsApi.putCompanyInfos(requestBody)

  apiProgressStore.saveSetting = false
}

// 企業情報一覧を設定前に戻す
const cancelCompanyInfosSetting = async () => {
  apiProgressStore.cancelSetting = true
  await getCompanyInfos()
  apiProgressStore.cancelSetting = false
}

// ユーザー情報取得
const getUser = async () => {
  const response = await meApi.getUserMe()
  csvDownloadType.value = response.payload.csvDownloadType
}

// ユーザーステータス更新
const updateUserStatus = async (patchUserMeStatus: PatchUserMeStatus) => {
  apiProgressStore.saveSetting = true
  const requestBody: PatchUserMeStatusRequest = {
    patchUserMeStatus: patchUserMeStatus,
  }

  await meApi.patchUserMeStatus(requestBody)
  apiProgressStore.saveSetting = false
}

// 「変更前に戻す」ボタンイベント
const cancelEvent = () => {
  if (settingsStore.mode === SettingsMode.CSV) {
    cancelCsvSetting()
  } else if (settingsStore.mode === SettingsMode.AUTH) {
    cancelAuthSetting()
  } else if (settingsStore.mode === SettingsMode.PAYMENT_CODE) {
    cancelPaymentCodeSetting()
  } else {
    cancelCompanyInfosSetting()
  }
}

// 「変更を保存」ボタンイベント
const saveEvent = async () => {
  if (settingsStore.mode === SettingsMode.CSV) {
    await updateUserStatus({ csvDownloadType: csvDownloadType.value })
    if (csvDownloadType.value === CsvDownloadType.ALLITEMS) updateCsvSetting()
  } else if (settingsStore.mode === SettingsMode.AUTH) {
    updateAuthSetting()
  } else if (settingsStore.mode === SettingsMode.PAYMENT_CODE) {
    updatePaymentCodeSetting()
  } else {
    updateCompanyInfosSetting()
  }
}

const getApi = async () => {
  await getCsvSettingMaster()
  await getAuthControl()
  await getPaymentCode()
  await getCompanyIntegrations()
  await getCompanyInfos()
  await getUser()
  loadingStore.loading = false
}
getApi()
</script>

<style lang="scss" scoped></style>
