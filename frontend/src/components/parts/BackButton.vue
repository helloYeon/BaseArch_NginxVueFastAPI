<template>
  <v-btn
    variant="outlined"
    color="#b11048"
    size="large"
    class="button"
    @click="back"
  >
    戻る
  </v-btn>
</template>

<script lang="ts" setup>
import { ROUTE_NAMES } from '@/const/const'
import { useReferrerStore } from '@/store/referrer'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const referrerStore = useReferrerStore()

// リファラから前回のページに遷移・なければInvoiceListに遷移
const back = () => {
  const prevRouteName = referrerStore.getPrevRefer?.name
  if (!prevRouteName || prevRouteName === route.name) {
    router.push({ name: ROUTE_NAMES.INVOICE_LIST })
    return
  }
  router.push({ name: prevRouteName })
}
</script>

<style lang="scss" scoped>
.button {
  font-size: 1.4rem;
}
</style>
