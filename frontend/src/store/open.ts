import { IsOpen } from '@/codegen'
import { defineStore } from 'pinia'

interface Open {
  isOpen: IsOpen
}

export const useOpenStore = defineStore('Open', {
  state: (): Open => ({
    isOpen: IsOpen.UNOPENED,
  }),
})
