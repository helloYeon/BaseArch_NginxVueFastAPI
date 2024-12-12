import { defineStore } from 'pinia'

interface Loading {
  loading: boolean
}

export const useLoadingStore = defineStore('loading', {
  state: (): Loading => ({
    loading: false,
  }),
})
