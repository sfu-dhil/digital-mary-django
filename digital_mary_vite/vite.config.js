import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    origin: 'http://localhost:5173',
    cors: 'http://localhost:8080',
  },
  root: resolve("./src"),
  base: "/static/dist/",
  build: {
    manifest: 'manifest.json',
    emptyOutDir: true,
    outDir: resolve("./dist"),
    rollupOptions: {
      input: {
        digital_mary: resolve('./src/digital_mary.js'),
      },
      globals: {
          jquery: 'window.jQuery',
          jquery: 'window.$'
      }
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: 'legacy'
      },
      sass: {
        api: 'legacy'
      },
    }
  },
  plugins: [],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
