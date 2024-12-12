<template>
  <tbody>
    <tr>
      <td v-for="n in columns" :key="n"></td>
    </tr>
  </tbody>
</template>

<script lang="ts" setup>
interface CommonEmptyTableRowProps {
  columns: number
}

defineProps<CommonEmptyTableRowProps>()
</script>

<style lang="scss" scoped>
td {
  border: 1px solid #e0e0e0;
}
</style>
