<template>
  <v-navigation-drawer class="header pb-2" permanent>
    <template #prepend>
      <CommonHeaderTitleLogo />

      <v-list v-model:opened="open">
        <v-list-item
          :active="activeListComputed"
          class="header__list"
          @click="transitionList"
        >
          <p class="header__list__title">文書表示</p>
        </v-list-item>
        <v-list-group value="Admin">
          <template #activator="{ props }">
            <v-list-item class="header__list" v-bind="props">
              <p class="header__list__title">管理者機能</p>
            </v-list-item>
          </template>

          <v-list-item
            class="header__list__settings"
            :active="activeSettingCsvComputed"
            @click="transitionSettings(SettingsMode.CSV)"
          >
            CSV出力項目設定
          </v-list-item>
          <v-list-item
            class="header__list__settings"
            :active="activeSettingAuthComputed"
            @click="transitionSettings(SettingsMode.AUTH)"
          >
            権限設定
          </v-list-item>
          <v-list-item
            class="header__list__settings"
            :active="activeSettingPaymentCodeComputed"
            @click="transitionSettings(SettingsMode.PAYMENT_CODE)"
          >
            支払先コード設定
          </v-list-item>
          <v-list-item
            v-if="isLocal() || isDevelopment()"
            class="header__list__settings"
            :active="activeSettingCompanyInfosComputed"
            @click="transitionSettings(SettingsMode.COMPANY_INFOS)"
          >
            企業統合設定
          </v-list-item>
        </v-list-group>
      </v-list>
    </template>

    <template #append>
      <v-list-item>
        <CommonUserInfo />
      </v-list-item>
    </template>
  </v-navigation-drawer>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSettingsStore, SettingsMode } from '@/store/settings'
import CommonHeaderTitleLogo from '@/components/templates/Common/CommonHeaderTitleLogo.vue'
import CommonUserInfo from '@/components/templates/Common/CommonUserInfo.vue'
import { ROUTE_NAMES } from '@/const/const'
import { isLocal, isDevelopment } from '@/utils'

const route = useRoute()
const router = useRouter()
const settingsStore = useSettingsStore()

const open = ref(route.name === ROUTE_NAMES.SETTINGS ? ['Admin'] : [])

const activeListComputed = computed(() => {
  return route.name === ROUTE_NAMES.INVOICE_LIST
})
const activeSettingCsvComputed = computed(() => {
  return (
    route.name === ROUTE_NAMES.SETTINGS &&
    settingsStore.mode === SettingsMode.CSV
  )
})
const activeSettingAuthComputed = computed(() => {
  return (
    route.name === ROUTE_NAMES.SETTINGS &&
    settingsStore.mode === SettingsMode.AUTH
  )
})
const activeSettingPaymentCodeComputed = computed(() => {
  return (
    route.name === ROUTE_NAMES.SETTINGS &&
    settingsStore.mode === SettingsMode.PAYMENT_CODE
  )
})
const activeSettingCompanyInfosComputed = computed(() => {
  return (
    route.name === ROUTE_NAMES.SETTINGS &&
    settingsStore.mode === SettingsMode.COMPANY_INFOS
  )
})

const transitionList = () => {
  router.push({ name: ROUTE_NAMES.INVOICE_LIST })
}
const transitionSettings = (mode: SettingsMode) => {
  settingsStore.mode = mode
  router.push({ name: ROUTE_NAMES.SETTINGS })
}
</script>

<style lang="scss" scoped>
.header {
  &__list {
    &__title {
      color: #222222;
      font-size: 1.6rem;
      font-weight: bold;
      margin-left: 12px;
    }

    &__settings {
      color: #222222;
      padding-left: 36px;
    }
  }
}
</style>
