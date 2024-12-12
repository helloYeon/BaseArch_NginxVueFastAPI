<template>
  <v-container
    v-if="csvTextMessage.length || noticeStore.getMessage.length"
    class="common-notice"
  >
    <div class="common-notice__content">
      <v-row
        v-for="message in csvTextMessage"
        :key="message"
        dense
        class="common-notice__row"
      >
        <v-icon :icon="NoticeIcon" size="small" class="mt-2" />
        <!-- eslint-disable-next-line vue/no-v-html -->
        <div class="v-col inner-html" v-html="message" />
      </v-row>
      <v-row
        v-for="message in noticeStore.getMessage"
        :key="message"
        dense
        class="common-notice__row common-notice__row--error"
      >
        <v-icon :icon="NoticeIcon" size="small" class="mt-2" />
        <v-col>{{ message }}</v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import { useNoticeStore } from '@/store/notice'
import {
  CSV_START_DATE_INDEX,
  CSV_START_TIME_INDEX,
  CSV_END_DATE_INDEX,
  CSV_END_TIME_INDEX,
  CSV_TEXT_INDEX,
} from '@/const/const'
import { ref } from 'vue'
import NoticeIcon from '@/components/parts/NoticeIcon.vue'

const noticeStore = useNoticeStore()

const csvTextMessage = ref<string[]>([])

const getCsvText = async () => {
  const response = await fetch(
    `${import.meta.env.VITE_S3_URL}/notices/notices.csv`
  )

  if (!response.ok) return

  const text = await response.text()

  const csvToArray = text
    .split(/\r\n|\n/)
    .map((s) => s.split(','))
    .splice(1)

  csvTextMessage.value = csvToArray
    .filter((row) => {
      return checkDate(
        row[CSV_START_DATE_INDEX],
        row[CSV_START_TIME_INDEX],
        row[CSV_END_DATE_INDEX],
        row[CSV_END_TIME_INDEX]
      )
    })
    .map((row) => row[CSV_TEXT_INDEX])
}

// 引数にundefinedがあればfalse返却
// 引数が空文字or現在の範囲であればtrue返却
const checkDate = (
  startDate: string,
  startTime: string,
  endDate: string,
  endTime: string
) => {
  if (
    [startDate, startTime, endDate, endTime].some(
      (value) => value === undefined
    )
  )
    return false

  const start = new Date(startDate + ' ' + startTime).getTime()
  const end = new Date(endDate + ' ' + endTime).getTime()
  const now = new Date().getTime()
  return (
    (Number.isNaN(start) || start <= now) && (Number.isNaN(end) || now <= end)
  )
}

noticeStore.$reset()

getCsvText()
</script>

<style lang="scss" scoped>
.common-notice {
  margin-top: 32px;
  &__content {
    padding: 16px;
    background-color: #f7efef;
    border-radius: 4px;
  }

  &__row {
    &--error {
      color: #b11048;
    }
  }

  .inner-html {
    &:deep(a) {
      text-decoration: underline;
    }
  }
}
</style>
