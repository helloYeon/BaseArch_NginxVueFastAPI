/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

// Global css
import '@/assets/styles/common.css'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
