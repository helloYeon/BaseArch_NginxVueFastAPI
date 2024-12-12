<template>
  <li
    class="setting-table__list"
    :class="{
      'setting-table__list--tree': indent,
      'setting-table__list--tree--last': lastChild,
    }"
  >
    <div
      class="setting-table__item"
      :class="{
        'setting-table__item--parent': !itemComputed.mstIsExistData,
      }"
    >
      <div
        v-if="itemComputed.child.length"
        class="setting-table__item__open-icon"
        @click.stop.prevent="open"
      >
        <v-icon v-if="!isOpen" icon="mdi-plus" />
        <v-icon v-if="isOpen" icon="mdi-minus" />
      </div>
      <p class="setting-table__item__name">
        {{ itemComputed.mstNameJp }}
      </p>
      <div class="setting-table__item__checkbox">
        <v-checkbox
          v-model="itemComputed.userIsDisplay"
          :true-value="1"
          :false-value="0"
          :indeterminate="itemComputed.indeterminate"
          density="compact"
          color="#b11048"
          hide-details
          @change="changeCheck"
        />
      </div>
    </div>

    <Transition v-if="itemComputed.child.length" name="open">
      <SettingsCsvTree
        v-show="isOpen"
        v-model:child="itemComputed.child"
        :parent-display="itemComputed.userIsDisplay"
        :indent="indent + 1"
      />
    </Transition>
  </li>
</template>

<script setup lang="ts">
import { computed, watch, watchEffect } from 'vue'
import { UserIsDisplay } from '@/codegen'
import { useNestedAccordionStore } from '@/store/nestedAccordion'
import { SettingListInterface } from '@/views/Settings.vue'
import SettingsCsvTree from '@/components/templates/Settings/SettingsCsv/SettingsCsvTree.vue'

interface InvoiceSettingItemProps {
  item: SettingListInterface
  indent: number
  lastChild: boolean
}

const props = withDefaults(defineProps<InvoiceSettingItemProps>(), {})

interface InvoiceSettingItemEmits {
  (e: 'update:item', item: SettingListInterface): void
}

const emit = defineEmits<InvoiceSettingItemEmits>()

const nestedAccordionStore = useNestedAccordionStore()

const isOpen = computed({
  get: () => nestedAccordionStore.getOpenList(props.item.mstPpolItemsId),
  set: (value) =>
    nestedAccordionStore.setOpenList(props.item.mstPpolItemsId, value),
})

const itemComputed = computed({
  get: () => props.item,
  set: (value) => emit('update:item', value),
})

const color = computed(() => {
  return itemComputed.value.mstIsExistData ? '#fff' : '#f6f6f6'
})

const padding = computed(() => {
  return `${props.indent * 16 + 16}px`
})

const left = computed(() => {
  return `${props.indent * 16 + 4}px`
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
  if (!itemComputed.value.mstIsExistData)
    updateCheckAllChild(
      itemComputed.value.child,
      itemComputed.value.userIsDisplay
    )
}

const open = () => {
  isOpen.value = !isOpen.value
}

// 子要素をwatch
// チェックボックス変更
watch(
  () => itemComputed.value.child,
  () => {
    // 子要素のチェックが全て同値かどうか判定
    // elseでチェックを0に固定
    if (
      itemComputed.value.child.every(
        ({ userIsDisplay }) =>
          userIsDisplay === itemComputed.value.child[0].userIsDisplay
      )
    ) {
      itemComputed.value.userIsDisplay =
        itemComputed.value.child[0].userIsDisplay
    } else {
      itemComputed.value.userIsDisplay = 0
    }
  },
  { deep: true }
)

watchEffect(() => {
  // 中間状態変更
  itemComputed.value.indeterminate =
    itemComputed.value.child.some(({ indeterminate }) => indeterminate) ||
    !itemComputed.value.child.every(
      ({ userIsDisplay }) =>
        userIsDisplay === itemComputed.value.child[0].userIsDisplay
    )
})
</script>

<style lang="scss" scoped>
.setting-table__list {
  position: relative;

  &--tree {
    &::before {
      content: '';
      position: absolute;
      top: -0.5em;
      left: v-bind(left);
      width: 10px;
      height: 100%;
      border-left: 2px double #e0e0e0;
      z-index: 2;
    }
    &--last::before {
      height: 2em;
    }

    &::after {
      content: '';
      position: absolute;
      top: 1.4em;
      left: v-bind(left);
      width: 10px;
      border-bottom: 2px double #e0e0e0;
      z-index: 2;
    }
  }

  .open-enter-active {
    animation: open 0.2s;
  }

  .open-leave-active {
    animation: open 0.2s linear reverse;
  }

  @keyframes open {
    0% {
      opacity: 0;
      transform: translateY(-5px);
    }

    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .rotate-enter-active {
    animation: rotate 0.2s linear;
  }

  @keyframes rotate {
    0% {
      transform: rotate(180deg);
    }
  }
}
.setting-table__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  padding-left: v-bind(padding);
  background-color: v-bind(color);
  border: 1px solid #e0e0e0;

  &--parent {
    box-shadow: 0px 0px 2px #000;
  }

  &__open-icon {
    margin-left: -4px;
    cursor: pointer;
  }

  &__name {
    flex: 1;
    max-height: 40px;
    margin-left: 8px;
    white-space: pre-wrap;
    font-size: 12px;
    cursor: grab;
    user-select: none;

    &:active {
      cursor: grabbing;
    }
  }

  &__checkbox {
    width: 80px;
    display: grid;
    justify-content: center;
    justify-items: center;
    border-left: 1px solid #e0e0e0;
  }
}
</style>
