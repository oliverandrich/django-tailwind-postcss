# Changelog

## 0.12.0

- Updated theme app template to Tailwind CSS 2.1 and changed the configuraton to use the new jit mode.
- Extended test suite to get 100% code coverage.
- Switched complete over to using pathlib instead of wild os.path.join constructs.

## 0.11.0

- Switched from watch to nodemon as a watcher. It now covers all the js, css and html files in your project.

## 0.10.0

- Fixed purge css configuration in tailwind.config.js to properly recurse into
  template folders of your own local apps too.
- Integrated the tailwindcss-jit compiler. Even though it is experimental, it works like a charm for me.
- **Breaking Change**: Restructured the structure of the app_template created by the tailwind command. You have to recreate your theme app, in order to use this version. Normally you just have to save your styles.css and copy it to the fresh app. In case you made changes to postcss.config.js or tailwind.config.js, copy these to the new app too.

## 0.9.2

- Added missing plugin references to postcss.config.js

## 0.9.1

- Fixed LICENSE to retain the original author.

## 0.9.0

- Forked [django-tailwind](https://github.com/timonweb/django-tailwind).
- Removed Sass and switched to a postcss only pipeline.
- Added @tailwindcss/aspect-ratio, @tailwindcss/forms and @tailwindcss/typography.
- Refactored the code base.
