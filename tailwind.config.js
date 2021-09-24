module.exports = {
  mode: 'jit',
  purge: [
    'main/templates/**/*.html',
    'main/home/templates/*.html',
    'main/example/templates/*.html',
    // './src/**/*.js',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
