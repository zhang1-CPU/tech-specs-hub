import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
  build: {
    outDir: './dist',
    rollupOptions: {
      input: {
        main: './assets/css/tailwind-entry.css',
      },
      output: {
        entryFileNames: '[name].css',
        assetFileNames: '[name].[ext]',
      },
    },
  },
})
