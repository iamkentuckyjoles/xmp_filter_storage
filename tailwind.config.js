/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './users/templates/**/*.html',
    './dashboard/templates/**/*.html',
    './event/templates/**/*.html',
    './static/**/*.js',
    './**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
}