<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    max-width="370px"
    min-width="auto"
  >
    <template #activator="{ props: on }">
      <v-text-field
        class="date-field"
        :model-value="formatDate(date)"
        v-bind="on"
        readonly
        clearable
        variant="outlined"
        density="compact"
        :error-messages="errorMessages"
        :placeholder="placeholder"
        append-inner-icon="mdi-calendar"
        @click:clear="clearInputDate"
      />
    </template>
    <v-date-picker
      v-model="date"
      hide-header
      show-adjacent-months
      width="100%"
      @update:model-value="closeDatePicker"
    />
  </v-menu>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { formatDate } from '@/plugins/utils'

interface InputDateProps {
  inputDate: Date | undefined
  placeholder: string
  errorMessages?: string
}

interface selectedDateEmits {
  (e: 'update:inputDate', date: Date | undefined): void
}

const props = withDefaults(defineProps<InputDateProps>(), {
  placeholder: '',
  errorMessages: undefined,
})

const emit = defineEmits<selectedDateEmits>()

const menu = ref(false)

const date = computed({
  get: () => props.inputDate,
  set: (value) => emit('update:inputDate', value),
})

const clearInputDate = () => {
  date.value = undefined
}

const closeDatePicker = () => {
  menu.value = false
}
</script>

<style lang="scss" scoped>
// カーソル変更
.date-field:deep(.v-field),
.date-field:deep(input) {
  cursor: pointer;
}
</style>
