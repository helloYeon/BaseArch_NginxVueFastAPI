import { defineStore } from 'pinia'

type isOpen = {
  [key: number]: boolean
}

interface NestedAccordionStore {
  openList: isOpen
}

export const useNestedAccordionStore = defineStore('nestedAccordion', {
  state: (): NestedAccordionStore => ({
    openList: {},
  }),
  getters: {
    getOpenList: (state) => (id: number) => state.openList?.[id] || false,
  },
  actions: {
    setOpenList(id: number, open: boolean) {
      this.openList[id] = open
    },
  },
})
