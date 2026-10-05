import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// O proxy repassa tudo que começa com /api para o backend Flask.
// Assim o navegador acha que frontend e API estão no mesmo endereço
// (localhost:5173), o cookie de sessão funciona sem complicação e não há problema de CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': process.env.API_URL || 'http://localhost:5001',
    },
  },
})
