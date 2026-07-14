const tailwindcss = require('tailwindcss');
const fs = require('fs');

const config = {
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
};

const input = `@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');`;

const result = tailwindcss.compile(input, {
  config: config,
  minify: true
});

console.log('Result keys:', Object.keys(result));
console.log('Result type:', typeof result);
console.log('Result:', JSON.stringify(result, null, 2).substring(0, 500));
