import { defineStore } from 'pinia'

export enum SettingsMode {
  CSV = 0,
  AUTH = 1,
  PAYMENT_CODE = 2,
  COMPANY_INFOS = 3, // テスト用
}

interface SettingsStore {
  mode: SettingsMode
}

export const useSettingsStore = defineStore('settings', {
  state: (): SettingsStore => ({
    mode: 0,
  }),
})
