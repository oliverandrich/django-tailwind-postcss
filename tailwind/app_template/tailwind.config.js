module.exports = {
  mode: "jit",
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
