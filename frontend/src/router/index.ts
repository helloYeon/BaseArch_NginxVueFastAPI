// Composables
import { createRouter, createWebHistory } from 'vue-router'

// Layout
import DefaultLayout from '@/layouts/default/Default.vue'

import { useReferrerStore } from '@/store/referrer'
import { ROUTE_NAMES } from '@/const/const'
import { useLoadingStore } from '@/store/loading'
import { isProduction } from '@/utils'

const commonRoutes = [
  {
    path: '/invoices',
    name: ROUTE_NAMES.INVOICE_LIST,
    meta: { layout: DefaultLayout },
    component: () => import('@/views/InvoiceList.vue'),
  },
  {
    path: '/invoices/:invoice_id(\\d+)',
    name: ROUTE_NAMES.INVOICE_DETAIL,
    meta: { layout: DefaultLayout },
    component: () => import('@/views/InvoiceDetail.vue'),
  },
  {
    path: '/settings',
    name: ROUTE_NAMES.SETTINGS,
    meta: { layout: DefaultLayout },
    component: () => import('@/views/Settings.vue'),
  },
  {
    path: '/auth_error',
    name: ROUTE_NAMES.UNAUTHORIZED,
    component: () => import('@/views/Common401Page.vue'),
  },
  {
    path: '/:pathMatch(.*)',
    name: ROUTE_NAMES.NOT_FOUND,
    component: () => import('@/views/Common404Page.vue'),
  },
  {
    path: '/error',
    name: ROUTE_NAMES.INTERNAL_SERVER_ERROR,
    component: () => import('@/views/Common500Page.vue'),
  },
]

const devRoutes = [
  {
    path: '/test_cookie',
    name: 'TestCookieSet',
    component: () => import('@/views/TestCookieSet.vue'),
  },
]

const routes = isProduction() ? commonRoutes : [...commonRoutes, ...devRoutes]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
      }
    }
    return { top: 0 }
  },
})

router.beforeEach(async (_to, from, next) => {
  const referrerStore = useReferrerStore()
  const loadingStore = useLoadingStore()
  loadingStore.loading = true
  // Todo: テストページから遷移した場合は遷移先の情報をリファラへセットする
  // （試験終わり次第if文削除！）
  if (from.name === 'TestCookieSet') {
    referrerStore.setPrevRefer(_to)
    next()
    return
  }

  // リファラセット
  referrerStore.setPrevRefer(from)
  next()
})

export default router
