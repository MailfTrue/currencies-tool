import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  resolve: { alias: { '@': '/src' } },
  server: {
    host: "0.0.0.0",
    port: 80,
    hmr: {clientPort: 8080},
    watch: {
      usePolling: true
    }
  },
  plugins: [vue()]
})
