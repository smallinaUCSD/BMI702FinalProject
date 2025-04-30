// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,          // ← allows Docker to bind to all IPs
    port: 5173,          // ← optional: set fixed port
    strictPort: true     // ← avoid port shuffling
  }
})
