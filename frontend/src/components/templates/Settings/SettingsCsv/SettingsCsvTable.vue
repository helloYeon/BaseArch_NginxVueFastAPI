<template>
  <ul>
    <li class="setting-table__head">
      <p class="setting-table__head__title">{{ type }}</p>
      <div class="setting-table__head__checkbox">
        <v-checkbox
          v-model="allCheck"
          :true-value="1"
          :false-value="0"
          :indeterminate="isIndeterminate"
          density="compact"
          color="#b11048"
          hide-details
          @change="changeCheck"
        />
        <p class="setting-table__head__checkbox__text">表示</p>
      </div>
    </li>
    <SettingsCsvTree
      v-model:child="settingListComputed"
      :parent-display="allCheck"
    />
  </ul>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { UserIsDisplay } from '@/codegen'
import { SettingListInterface } from '@/views/Settings.vue'
import SettingsCsvTree from '@/components/templates/Settings/SettingsCsv/SettingsCsvTree.vue'

interface InvoiceSettingTableProps {
  settingList: SettingListInterface[]
  type: string
}

const props = defineProps<InvoiceSettingTableProps>()

interface InvoiceSettingTableEmits {
  (e: 'update:settingList', settingList: SettingListInterface[]): void
}

const emit = defineEmits<InvoiceSettingTableEmits>()

const allCheck = ref<UserIsDisplay>(0)

const settingListComputed = computed({
  get: () => props.settingList,
  set: (value) => emit('update:settingList', value),
})

// 中間状態返却
const isIndeterminate = computed(() => {
  return (
    settingListComputed.value.some(({ indeterminate }) => indeterminate) ||
    !settingListComputed.value.every(
      ({ userIsDisplay }) =>
        userIsDisplay === settingListComputed.value[0].userIsDisplay
    )
  )
})

// 子要素のチェック状態を全て変更
const updateCheckAllChild = (
  child: SettingListInterface[],
  userIsDisplay: UserIsDisplay
) => {
  child.forEach((item) => {
    item.userIsDisplay = userIsDisplay

    // 子要素があれば再帰的に処理
    if (!item.mstIsExistData)
      updateCheckAllChild(item.child, item.userIsDisplay)
  })
}

// チェック押下時発火
const changeCheck = () => {
  updateCheckAllChild(settingListComputed.value, allCheck.value)
}

// 初回実行
// 子要素をwatch
// チェックボックス変更
watch(
  () => settingListComputed.value,
  () => {
    if (
      settingListComputed.value.every(
        ({ userIsDisplay }) =>
          userIsDisplay === settingListComputed.value[0].userIsDisplay
      )
    ) {
      allCheck.value = settingListComputed.value[0].userIsDisplay
    } else {
      allCheck.value = 0
    }
  },
  { immediate: true, deep: true }
)
</script>

<style lang="scss" scoped>
.setting-table__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 2px solid #e0e0e0;
  background-color: #f6f6f6;

  &__title {
    padding-left: 8px;
    font-size: 1.6rem;
    font-weight: bold;
  }

  &__checkbox {
    width: 80px;
    display: grid;
    align-items: center;
    justify-content: center;
    justify-items: center;
    grid-template-columns: 40% 40%;
    border-left: 2px solid #e0e0e0;

    &__text {
      font-weight: bold;
    }
  }
}
</style>
