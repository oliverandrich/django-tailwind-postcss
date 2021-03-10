# Django + Tailwind = ❤

This is a fork of the great project [django-tailwind](https://github.com/timonweb/django-tailwind) by [timonweb](https://github.com/timonweb). Instead of using [Sass](https://sass-lang.com) in the css procesing pipeline, I prefer to stick to a postcss only pipeline and also integrated the officials plugins, that are recommended by [Tailwind UI](https://tailwindui.com). I also took the decision to strip the support for Tailwind CSS 1.x. In order to support nested rules in the css definitions, [postcss-nested](https://github.com/postcss/postcss-nested) is also added.

## Installation

1. Install the `django-tailwind` package via Pip:

   `python -m pip install django-tailwind`

2. Add `tailwind` to INSTALLED_APPS in **settings.py**

3. Create a tailwind-compatible Django-app, I like to call it `theme`:

   `python manage.py tailwind init theme`

4. Add your newly created `theme` app to INSTALLED_APPS in **settings.py**

5. In settings.py, register tailwind app by adding the following string:

   `TAILWIND_APP_NAME = 'theme'`

6. Run a command to install all necessary dependencies for tailwind css:

   `python manage.py tailwind install`

7. Now, go and start tailwind in dev mode:

   `python manage.py tailwind start`

8. Django Tailwind comes with a simple `base.html` template that can be found under
   `theme/templates/base.html`. Feel free to extend it as needed. If you don't want
   to use the default template, you have add the link for styles.css manually to
   your base template.

   ```html
   <link
     rel="stylesheet"
     href="{% static 'css/styles.css' %}"
     type="text/css"
   />
   ```

## Production Builds

To build a production version of CSS run:

```
python manage.py tailwind build
```

## Adding your custom base styles, components and utilities

In order to define your on base styles, components and utilties as described in the documents [Adding Base Styles](https://tailwindcss.com/docs/adding-base-styles), [Extracting Components](https://tailwindcss.com/docs/extracting-components#extracting-component-classes-with-apply) and [Adding New Utilities](https://tailwindcss.com/docs/adding-new-utilities), just add them the corresponding layers defined in `theme/static_src/src/styles.css`.

## PurgeCSS setup

To avoid importing all of Tailwind (resulting in a massive CSS filesize),
set up the purge configuration in `tailwind.config.js`. This file is located
in the `static_src` folder of the app created by `tailwind init {APP_NAME}`.

```js
module.exports = {
  purge: [
    // Templates within theme app (e.g. base.html)
    '../templates/**/*.html',
    // Templates in other apps
    '../../templates/**/*.html',
  ],
  ...
}
```

Note that you may need to adjust those paths to suit your specific project layout. It is important to ensure that _all_ of your HTML files are covered (or files with contain HTML content, such as .vue or .jsx files), to enusre PurgeCSS can whitelist all of your classes.

For more information on this, check out the "Controlling File Size" page of the Tailwind docs: [https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css](https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css) - particularly the "Removing Unused CSS" section, although the entire page is a useful reference.

To help speed up development builds, PurgeCSS is only run when you use the `tailwind build` management command (to create a production build of your CSS).

## NPM executable path configuration

Sometimes (especially on Windows), Python executable can't find `NPM` installed in the system.
In this case, you need to set `NPM` executable path in settings.py file manually (Linux/Mac):

```python
NPM_BIN_PATH = '/usr/local/bin/npm'
```

On windows it might look like:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Please note that `NPM` path of your system may be different. Try to run `which npm` in your
command line to get the path.

## Updating Tailwind CSS and dependencies

If there's a new release of the tailwind css came out you can always update your `theme` project
without updating this django package by using two commands: `python manage.py tailwind check-updates` and `python manage.py tailwind update`.

## Bugs and suggestions

If you have found a bug, please use the issue tracker on GitHub.

[https://github.com/oliverandrich/django-tailwind-postcss/issues](https://github.com/timonweb/django-tailwind/issues)
