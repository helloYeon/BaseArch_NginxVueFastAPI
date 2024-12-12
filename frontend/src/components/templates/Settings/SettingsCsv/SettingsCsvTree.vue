<template>
  <draggable
    v-model="childComputed"
    tag="ul"
    item-key="mstPpolItemsId"
    handle=".setting-table__item__name"
    :animation="500"
    :force-fallback="true"
  >
    <template #item="{ index }">
      <SettingsCsvItem
        v-model:item="childComputed[index]"
        :indent="indent"
        :last-child="index === childComputed.length - 1"
      />
    </template>
  </draggable>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import draggable from 'vuedraggable'
import { UserIsDisplay } from '@/codegen'
import { SettingListInterface } from '@/views/Settings.vue'
import SettingsCsvItem from '@/components/templates/Settings/SettingsCsv/SettingsCsvItem.vue'

interface InvoiceSettingTreeProps {
  child: SettingListInterface[]
  parentDisplay: UserIsDisplay
  indent?: number
}

const props = withDefaults(defineProps<InvoiceSettingTreeProps>(), {
  indent: 0,
})

interface InvoiceSettingTableEmits {
  (e: 'update:child', child: SettingListInterface[]): void
}

const emit = defineEmits<InvoiceSettingTableEmits>()

const childComputed = computed({
  get: () => props.child,
  set: (value) => emit('update:child', value),
})
</script>

<style lang="scss" scoped>
// vueDraggable専用クラス
// drag中DOMに付与
.sortable-chosen {
  background-color: #f7efef;

  // コンポーネント配下のクラス指定
  &:deep(.setting-table__item) {
    background-color: transparent;
  }
}
</style>
