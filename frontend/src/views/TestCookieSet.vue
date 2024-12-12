<template>
  <div></div>
</template>

<script lang="ts" setup>
import { InfoApi } from '@/codegen'
import { ROUTE_NAMES } from '@/const/const'
import { ClientConfig } from '@/plugins/apiClient'
import { useGetInvoicesRequestStore } from '@/store/getInvoicesRequest'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const requestStore = useGetInvoicesRequestStore()

const infoApi = new InfoApi(new ClientConfig())

/**
 * 試験：正常系テスト用クッキー取得
 * 開発環境でのみ遷移可能
 */
const value = String(route.query.cookies_computer_es)
const domain = String(route.query.cookies_domain)
document.cookie = `cookies%5Fcomputer%5Fes=${value}; path=/; domain=${domain}; Secure; SameSite=none`

const routerPush = async () => {
  // 請求書情報画面遷移時のみ請求書IDが必要なので
  // 一覧取得APIから一番最初の請求書IDを取得してから遷移
  if (route.query.transition === ROUTE_NAMES.INVOICE_DETAIL) {
    const { payload } = await infoApi.getInvoices(requestStore.getRequest)
    router.push({
      name: String(route.query.transition),
      params: { invoice_id: payload.items[0].invoiceId },
    })
    return
  }

  router.push({
    name: String(route.query.transition),
  })
}
routerPush()
</script>
