/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  corePlugins: {
    // Disable Preflight so Tailwind doesn't conflict with existing index.css reset
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        sidebar: '#13151f',
        surface: '#1a1d27',
        'surface-hover': '#22263a',
        border: '#2a2d3e',
      },
    },
  },
  plugins: [],
}
