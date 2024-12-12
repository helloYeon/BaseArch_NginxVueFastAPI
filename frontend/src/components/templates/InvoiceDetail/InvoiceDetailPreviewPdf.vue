<template>
  <v-card color="#404040" width="100%" class="mt-8 ml-auto mr-auto">
    <v-card-title class="title d-flex justify-end align-center my-4">
      <div v-if="pdfData" class="d-flex align-center vertical-border">
        <InvoiceDetailPreviewIconButton
          title="前のページへ"
          icon="mdi-chevron-left"
          :disabled="isFirstPage"
          @click="prevButton"
        />
        <p>
          <input
            v-model="page"
            class="page-number"
            type="text"
            title="ページ"
            autocomplete="off"
            @input="inputPageFormat"
          />
          / {{ pages }}
        </p>
        <InvoiceDetailPreviewIconButton
          title="次のページへ"
          icon="mdi-chevron-right"
          :disabled="isLastPage"
          @click="nextButton"
        />
      </div>
      <div v-if="pdfData" class="d-flex align-center vertical-border">
        <InvoiceDetailPreviewIconButton
          title="縮小"
          icon="mdi-minus"
          :disabled="isMinScale"
          @click="reductionButton"
        />
        <p>
          <v-select
            v-model="scale"
            :items="PDF_SIZE_ITEMS"
            item-title="text"
            variant="outlined"
            density="compact"
            theme="dark"
            hide-details
          />
        </p>
        <InvoiceDetailPreviewIconButton
          title="拡大"
          icon="mdi-plus"
          :disabled="isMaxScale"
          @click="expansionButton"
        />
      </div>
      <div v-if="pdfData" class="d-flex align-center vertical-border">
        <InvoiceDetailPreviewIconButton
          title="全画面表示"
          icon="mdi-arrow-expand-all"
          @click="fullscreenButton"
        />
      </div>
      <div v-if="pdfData" class="d-flex align-center custom-download-button">
        <InvoiceDetailPreviewIconButton
          title="PDFをダウンロードする"
          icon="mdi-tray-arrow-down"
          @click="emit('download')"
        />
      </div>
    </v-card-title>
    <v-card-text class="v-card-text">
      <VuePDF
        ref="vuePdf"
        :pdf="pdf"
        :page="checkedPage"
        :height="heightComputed"
        :scale="scale"
        class="vue-pdf"
        @click="pdfClickInFullscreen"
        @wheel="pdfWheelInFullscreen"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { VuePDF, usePDF } from '@tato30/vue-pdf'
import { useFullscreen } from '@vueuse/core'
import InvoiceDetailPreviewIconButton from './InvoiceDetailPreviewIconButton.vue'
import { PDF_SIZE_ITEMS } from '@/const/const'

interface PreviewPdfProps {
  pdfData: Blob
}

interface PreviewPdfEmits {
  (e: 'download'): void
}

const props = defineProps<PreviewPdfProps>()
const emit = defineEmits<PreviewPdfEmits>()

const page = ref('1')
const height = ref()
const scale = ref(1)
const vuePdf = ref<HTMLElement | null>(null)

const pdfDataUrlComputed = computed(() => {
  return props.pdfData ? URL.createObjectURL(props.pdfData) : ''
})

const { pdf, pages } = usePDF(pdfDataUrlComputed)
const { isFullscreen, toggle } = useFullscreen(vuePdf)

// 通常はScaleで大きさ管理
// フルスクリーン時のみheightを使用
const heightComputed = computed(() => {
  if (isFullscreen.value) {
    return height.value
  }
  return undefined
})

const pageComputed = computed(() => {
  return Number(page.value)
})

const isFirstPage = computed(() => {
  return pageComputed.value === 1 ? true : false
})
const isLastPage = computed(() => {
  return pageComputed.value === pages.value ? true : false
})

const isMinScale = computed(() => {
  return scale.value === 0.5 ? true : false
})
const isMaxScale = computed(() => {
  return scale.value === 4 ? true : false
})

// pageの整合性チェック
const checkedPage = computed(() => {
  if (1 <= pageComputed.value && pageComputed.value <= pages.value)
    return pageComputed.value
  return 1
})

// ページ入力時のフォーマット
const inputPageFormat = () => {
  if (pageComputed.value > pages.value) {
    page.value = String(pages.value)
  }

  // 小数点、数字以外の文字排除
  page.value = page.value.replace(/[^0-9]/g, '').replace(/\D/g, '')
}

// 戻るボタン
const prevButton = () => {
  page.value = String(
    pageComputed.value > 1 ? pageComputed.value - 1 : pageComputed.value
  )
}
// 次へボタン
const nextButton = () => {
  page.value = String(
    pageComputed.value < pages.value
      ? pageComputed.value + 1
      : pageComputed.value
  )
}

// サイズ縮小
const reductionButton = () => {
  scale.value = scale.value > 0.5 ? scale.value - 0.25 : scale.value
}
// サイズ拡大
const expansionButton = () => {
  scale.value = scale.value < 4 ? scale.value + 0.25 : scale.value
}

// フルスクリーン処理
const fullscreenButton = () => {
  height.value = screen.height
  toggle()
}

// フルスクリーン状態時に左クリックで次ページ移動処理
const pdfClickInFullscreen = () => {
  if (!isFullscreen.value) {
    return
  }
  nextButton()
}
// フルスクリーン状態時にホイールでページネーション処理
const pdfWheelInFullscreen = (wheelEvent: WheelEvent) => {
  if (!isFullscreen.value) {
    return
  }

  if (wheelEvent.deltaY > 0) {
    nextButton()
  }
  if (wheelEvent.deltaY < 0) {
    prevButton()
  }
}
</script>

<style lang="scss" scoped>
.icon {
  opacity: 0.7;
  margin: 2px 1px;
  padding: 2px 6px 0;

  &:hover {
    background-color: #666667;
  }
}

.page-number {
  text-align: center;
  width: 24px;
  background-size: 0 0;
  transition-property: none;
  margin: 3px 0;
  border-radius: 2px;
  background-color: #404044;
  background-clip: padding-box;
  border: 1px solid #737373;
  box-shadow: none;
  color: #fafafa;
  appearance: textField;
  -moz-appearance: textfield;

  &::-webkit-inner-spin-button,
  &::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
}

.vertical-border {
  border-right: 1px solid #0000004d;
}

.custom-download-button {
  min-width: 16px;
  margin: 2px 1px;
  width: 38px;
  height: 16px;
  padding: 2px 6px 0;
  border: none;
  border-radius: 2px;
}

.v-card-text {
  height: 1100px;
  overflow: auto;
}

.vue-pdf {
  width: fit-content;
  margin: 0 auto;

  // フルスクリーン時にPDFが中央になるよう調整
  &:deep(canvas) {
    margin: 0 auto;
  }
}
</style>
