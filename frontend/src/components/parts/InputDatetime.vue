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
        :model-value="formatDate(datetime, 'yyyy/MM/dd HH:mm')"
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
      v-model="datetime"
      class="date-picker"
      hide-header
      show-adjacent-months
      width="100%"
      @update:model-value="closeDatePicker"
    />
    <div class="date-picker__time-picker">
      <v-select
        v-model="hours"
        class="date-picker__time-picker__select"
        :items="HOURS_ARRAY"
        variant="outlined"
        density="compact"
        @update:model-value="setHours"
      >
      </v-select>
      <v-select
        v-model="minutes"
        class="date-picker__time-picker__select"
        :items="MINUTES_ARRAY"
        variant="outlined"
        density="compact"
        @update:model-value="setMinutes"
      />
    </div>
  </v-menu>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { formatDate } from '@/plugins/utils'
import { HOURS_ARRAY, MINUTES_ARRAY } from '@/const/datetime'

interface InputDatetimeProps {
  inputDatetime: Date | undefined
  placeholder: string
  errorMessages?: string
}

interface selectedDatetimeEmits {
  (e: 'update:inputDatetime', datetime: Date | undefined): void
}

const props = withDefaults(defineProps<InputDatetimeProps>(), {
  placeholder: '',
  errorMessages: undefined,
})

const emit = defineEmits<selectedDatetimeEmits>()

const menu = ref(false)

const hours = ref(props.inputDatetime?.getHours() ?? 0)
const minutes = ref(props.inputDatetime?.getMinutes() ?? 0)

const datetime = computed({
  get: () => props.inputDatetime,
  set: (value) => {
    if (value) {
      value.setHours(hours.value)
      value.setMinutes(minutes.value)
    }
    emit('update:inputDatetime', value)
  },
})

// 時間をセット
const setHours = () => {
  if (!datetime.value) return
  datetime.value.setHours(hours.value)
  emit('update:inputDatetime', datetime.value)
}
// 分をセット
const setMinutes = () => {
  if (!datetime.value) return
  datetime.value.setMinutes(minutes.value)
  emit('update:inputDatetime', datetime.value)
}

// クリアアイコン押下時の処理
const clearInputDate = () => {
  datetime.value = undefined
  hours.value = 0
  minutes.value = 0
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

.date-picker {
  padding-bottom: 60px;
  position: relative;

  &__time-picker {
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    bottom: 0;
    height: 60px;
    width: 100%;

    &__select {
      margin: 0 16px;

      &:first-child {
        margin-right: 0;
      }
    }
  }
}
</style>
