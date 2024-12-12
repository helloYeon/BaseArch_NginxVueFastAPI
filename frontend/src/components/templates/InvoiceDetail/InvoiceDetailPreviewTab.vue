<template>
  <InvoiceDetailGeneratePdf
    ref="generatePdf"
    :pdf-data="pdfData"
    @pdf-data="pdfDataEmit"
  />
  <InvoiceDetailPreviewPdf :pdf-data="pdf" @download="emit('download', pdf)" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import InvoiceDetailGeneratePdf from '@/components/templates/InvoiceDetail/InvoiceDetailGeneratePdf.vue'
import InvoiceDetailPreviewPdf from '@/components/templates/InvoiceDetail/InvoiceDetailPreviewPdf.vue'
import { Preview } from '@/codegen'

interface PreviewProps {
  pdfData: Preview
}

interface PreviewEmits {
  (e: 'download', pdf: Blob): void
}

defineProps<PreviewProps>()
const emit = defineEmits<PreviewEmits>()

const pdf = ref()
const pdfDataEmit = (data: Blob) => {
  pdf.value = data
}
</script>
