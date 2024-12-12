import { defineStore } from 'pinia'

interface ApiProgress {
  invoices: boolean
  invoicesSearch: boolean
  csv: boolean
  receive: boolean
  confirm: boolean
  download: boolean
  xml: boolean
  detail: boolean
  cancelSetting: boolean
  saveSetting: boolean
}

export const useApiProgressStore = defineStore('apiProgress', {
  state: (): ApiProgress => ({
    // 一覧画面
    invoices: false,
    invoicesSearch: false,
    csv: false,
    receive: false,
    // 詳細画面
    confirm: false,
    download: false,
    xml: false,
    detail: false,
    // 設定画面
    cancelSetting: false,
    saveSetting: false,
  }),
})
