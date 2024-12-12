// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import ViteFonts from 'unplugin-fonts/vite'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import * as dotenv from 'dotenv'

const environment = process.env.APP_ENV

// eslint-disable-next-line @typescript-eslint/no-var-requires
const env = dotenv.config({ path: `./src/env/.env.${environment}` })
if (env.error) {
  throw env.error
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({ template: { transformAssetUrls } }),
    vuetify({
      styles: {
        configFile: 'src/assets/styles/settings.scss',
      },
    }),
    ViteFonts({
      google: {
        families: [
          {
            name: 'Roboto',
            styles: 'wght@100;300;400;500;700;900',
          },
        ],
      },
    }),
  ],
  define: { 'process.env': { env } },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
    extensions: ['.js', '.json', '.jsx', '.mjs', '.ts', '.tsx', '.vue'],
  },
  server: {
    port: 80,
    host: true,
    // ホットリロードを有効化するため監視を強制
    watch: {
      usePolling: true,
    },
  },
})
