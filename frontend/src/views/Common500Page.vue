<template>
  <CommonErrorTextContent>
    <p>エラーが発生しました</p>
    <v-btn
      variant="outlined"
      class="button font-weight-bold w-75 mt-4"
      @click="homeButton"
    >
      ホームへ
    </v-btn>
  </CommonErrorTextContent>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import CommonErrorTextContent from '@/components/templates/Common/CommonErrorTextContent.vue'
import { ROUTE_NAMES } from '@/const/const'
import { useLoadingStore } from '@/store/loading'

const router = useRouter()
const loadingStore = useLoadingStore()

loadingStore.loading = false
const homeButton = () => {
  router.push({ name: ROUTE_NAMES.INVOICE_LIST })
}
</script>

<style lang="scss" scoped>
.button {
  font-size: 1.5rem;
}
</style>
