/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// Vuetify
import DateFnsAdapter from '@date-io/date-fns'
import { ja } from 'date-fns/locale'

// Components
import { VBtn } from 'vuetify/components/VBtn'
import { VApp } from 'vuetify/components/VApp'
import { VMenu } from 'vuetify/components/VMenu'
import { VTextField } from 'vuetify/components/VTextField'
import { VSelect } from 'vuetify/components/VSelect'
import { VDatePicker } from 'vuetify/components/VDatePicker'
import { VDialog } from 'vuetify/components/VDialog'
import {
  VCard,
  VCardActions,
  VCardItem,
  VCardTitle,
  VCardText,
} from 'vuetify/components/VCard'
import { VFooter } from 'vuetify/components/VFooter'
import { VDivider } from 'vuetify/components/VDivider'
import { VContainer, VRow, VCol, VSpacer } from 'vuetify/components/VGrid'
import { VNavigationDrawer } from 'vuetify/components/VNavigationDrawer'
import { VList, VListItem, VListItemTitle } from 'vuetify/components/VList'
import { VIcon } from 'vuetify/components/VIcon'
import {
  VExpansionPanels,
  VExpansionPanel,
  VExpansionPanelTitle,
  VExpansionPanelText,
} from 'vuetify/components/VExpansionPanel'
import { VTable } from 'vuetify/components/VTable'
import { VSheet } from 'vuetify/components/VSheet'
import { VChip } from 'vuetify/components/VChip'
import { VForm } from 'vuetify/components/VForm'
import { VPagination } from 'vuetify/components/VPagination'
import { VCheckbox } from 'vuetify/components/VCheckbox'
import { VImg } from 'vuetify/components/VImg'
import {
  VOverlay,
  VProgressCircular,
  VSnackbar,
} from 'vuetify/lib/components/index.mjs'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  date: {
    adapter: new DateFnsAdapter({
      formats: {
        year: 'yyyy年',
        monthAndYear: 'yyyy年M月',
        normalDateWithWeekday: 'M月d日(E)',
      },
      locale: ja,
    }),
  },
  components: {
    VBtn,
    VApp,
    VMenu,
    VTextField,
    VSelect,
    VDatePicker,
    VDialog,
    VCard,
    VCardActions,
    VCardItem,
    VCardTitle,
    VCardText,
    VFooter,
    VDivider,
    VContainer,
    VRow,
    VCol,
    VSpacer,
    VNavigationDrawer,
    VList,
    VListItem,
    VListItemTitle,
    VIcon,
    VExpansionPanels,
    VExpansionPanel,
    VExpansionPanelTitle,
    VExpansionPanelText,
    VTable,
    VSheet,
    VChip,
    VForm,
    VPagination,
    VCheckbox,
    VImg,
    VOverlay,
    VProgressCircular,
    VSnackbar,
  },
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
  },
})
