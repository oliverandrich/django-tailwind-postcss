// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
  purge: [
    "./templates/**/*.html",
    "../templates/**/*.html",
    "../**/templates/**/*.html",
  ],
  darkMode: "media", // or 'class' or false
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
