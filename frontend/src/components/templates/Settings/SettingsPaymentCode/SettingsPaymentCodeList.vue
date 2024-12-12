<template>
  <v-row>
    <v-col>
      <v-row no-gutters class="list-content">
        <v-col>
          <v-list
            v-model:selected="selectedPeppolIdsComputed"
            density="compact"
            select-strategy="classic"
            class="list"
          >
            <v-list-item class="list__header">
              <v-row>
                <v-col
                  class="list__header__title"
                  @click="sort(PaymentCodeSort.PeppolId)"
                  >PeppolId
                  <span
                    class="sort"
                    :class="sortClass(PaymentCodeSort.PeppolId)"
                  >
                    <v-icon end icon="mdi-menu-up menu-up-icon" />
                    <v-icon end icon="mdi-menu-down menu-down-icon" />
                  </span>
                </v-col>
                <v-divider thickness="2" vertical></v-divider>
                <v-col
                  class="list__header__title"
                  @click="sort(PaymentCodeSort.PaymentCode)"
                  >支払先コード
                  <span
                    class="sort"
                    :class="sortClass(PaymentCodeSort.PaymentCode)"
                  >
                    <v-icon end icon="mdi-menu-up menu-up-icon" />
                    <v-icon end icon="mdi-menu-down menu-down-icon" />
                  </span>
                </v-col>
              </v-row>
            </v-list-item>
            <v-divider thickness="3"></v-divider>
            <v-list-item
              v-for="item in paymentCodeList"
              :key="item.peppolId"
              :value="item.peppolId"
              density="compact"
              color="primary"
            >
              <v-row>
                <v-col>{{ item.peppolId }}</v-col>
                <v-divider thickness="2" vertical></v-divider>
                <v-col>{{ item.paymentCode }}</v-col>
              </v-row>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { PaymentCodeData } from '@/codegen'
import {
  usePaymentCodeStore,
  PaymentCodeSort,
  PaymentCodeSortOrder,
} from '@/store/paymentCode'
import { computed } from 'vue'

interface SettingsPaymentCodeListProps {
  paymentCodeList: PaymentCodeData[]
  selectedPeppolIds: string[]
}

interface SettingsPaymentCodeListEmits {
  (e: 'update:selectedPeppolIds', page: string[]): void
  (e: 'sort'): void
}

const props = defineProps<SettingsPaymentCodeListProps>()
const emit = defineEmits<SettingsPaymentCodeListEmits>()

const paymentCodeStore = usePaymentCodeStore()

const selectedPeppolIdsComputed = computed({
  get: () => props.selectedPeppolIds,
  set: (value) => emit('update:selectedPeppolIds', value),
})

// ソート利用時のcss制御
const sortClass = (sort: PaymentCodeSort) => {
  return {
    asc:
      paymentCodeStore.sort === sort &&
      paymentCodeStore.sortOrder === PaymentCodeSortOrder.ASC,
    desc:
      paymentCodeStore.sort === sort &&
      paymentCodeStore.sortOrder === PaymentCodeSortOrder.DESC,
  }
}

// ソートの値をstoreにセットする
const sort = (sort: PaymentCodeSort) => {
  if (paymentCodeStore.sort === sort) {
    paymentCodeStore.sortOrder =
      paymentCodeStore.sortOrder === PaymentCodeSortOrder.ASC
        ? PaymentCodeSortOrder.DESC
        : PaymentCodeSortOrder.ASC
  } else {
    paymentCodeStore.sort = sort
    paymentCodeStore.sortOrder = PaymentCodeSortOrder.ASC
  }
  emit('sort')
}
</script>

<style lang="scss" scoped>
.list-content {
  background-color: #fff;
}

.list {
  height: 400px;
  overflow-y: auto;
  &__header {
    &__title {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    .sort {
      display: flex;
      flex-direction: column;
      .menu-up-icon {
        bottom: -6px;
      }
      .menu-down-icon {
        top: -6px;
      }
      &.desc .menu-up-icon {
        opacity: 0.3;
      }
      &.asc .menu-down-icon {
        opacity: 0.3;
      }
    }
  }
}
</style>
