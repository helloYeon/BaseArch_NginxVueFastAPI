import { defineStore } from 'pinia'
import { RouteLocationNormalized } from 'vue-router'

interface ReferrerStore {
  prevRefer: RouteLocationNormalized | null
}

export const useReferrerStore = defineStore('referrer', {
  state: (): ReferrerStore => ({
    prevRefer: null,
  }),
  getters: {
    getPrevRefer: (state) => state.prevRefer,
  },
  actions: {
    setPrevRefer(prevRefer: RouteLocationNormalized) {
      this.prevRefer = prevRefer
    },
  },
})
