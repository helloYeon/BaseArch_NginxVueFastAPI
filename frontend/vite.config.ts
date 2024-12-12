// Plugins
import vue from '@vitejs/plugin-vue'

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
  plugins: [vue()],
  define: { 'process.env': { env } },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 8081,
    host: true,
    // ホットリロードを有効化するため監視を強制
    watch: {
      usePolling: true,
    },
  },
})
