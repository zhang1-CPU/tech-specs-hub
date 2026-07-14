/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./pages/**/*.html",
    "./assets/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        navy: { 
          950: '#0a1628', 
          900: '#0f1d32', 
          800: '#162544', 
          700: '#1e3259' 
        },
        electric: { 
          300: '#67e8f9', 
          400: '#22d3ee', 
          500: '#06b6d4', 
          600: '#0891b2' 
        }
      },
      fontFamily: {
        display: ['Space Grotesk', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      }
    }
  },
  plugins: []
}
