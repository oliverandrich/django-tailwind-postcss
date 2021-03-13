import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError, LabelCommand

usage = """
Command argument is missing, please add one of the following:
  init - to initialize django-tailwind app
  install - to install npm packages necessary to build tailwind css
  build - to compile tailwind css into production css
  start - to start watching css changes for dev
  check-updates - to list possible updates for tailwind css and its dependencies
  update - to update tailwind css and its dependencies
Usage example:
  python manage.py tailwind start
"""


class Command(LabelCommand):
    help = "Runs tailwind commands"
    missing_args_message = usage

    def validate_app(self):
        if not hasattr(settings, "TAILWIND_APP_NAME"):
            raise CommandError("TAILWIND_APP_NAME isn't set in settings.py")

        app_name = getattr(settings, "TAILWIND_APP_NAME")

        if not apps.is_installed(app_name):
            raise CommandError(f"{app_name} is not in INSTALLED_APPS")

        if not os.path.isfile(os.path.join(self._get_tailwind_src_path(), "tailwind.config.js")):
            raise CommandError(f"'{app_name}' isn't a Tailwind app")

    def handle(self, *labels, **options):
        label = labels[0]
        if labels[0] not in [
            "init",
            "install",
            "npm",
            "start",
            "build",
            "check-updates",
            "update",
        ]:
            raise Exception(f"Subcommand {label} doesn't exist")

        if label != "init":
            self.validate_app()

        getattr(self, "handle_" + label.replace("-", "_") + "_command")(*labels[1:], **options)

    def handle_init_command(self, app_name, **options):
        try:
            app_template_path = os.path.join(
                Path(__file__).resolve().parent.parent.parent, "app_template"
            )
            call_command("startapp", app_name, template=app_template_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Tailwind application successfully created. "
                    f"Please add '{app_name}' to INSTALLED_APPS in settings.py."
                )
            )
        except Exception as err:
            raise CommandError(err)

    def handle_install_command(self, **options):
        self.npm_command("install")

    def handle_build_command(self, **options):
        self.npm_command("run", "build")

    def handle_start_command(self, **options):
        self.npm_command("run", "start")

    def handle_check_updates_command(self, **options):
        self.npm_command("outdated")

    def handle_update_command(self, **options):
        self.npm_command("update")

    def npm_command(self, *args):
        try:
            npm_bin_path = getattr(settings, "NPM_BIN_PATH", "npm")
            subprocess.run([npm_bin_path] + list(args), cwd=self._get_tailwind_src_path())
        except OSError:
            raise CommandError(
                "\nIt looks like node.js and/or npm is not installed or cannot be found.\n\n"
                "Visit https://nodejs.org to download and install node.js for your system.\n\n"
                "If you have npm installed and still getting this error message, "
                "set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.\n\n"
                ""
                "Example:\n"
                'NPM_BIN_PATH = "/usr/local/bin/npm"'
            )
        except KeyboardInterrupt:
            pass

    def _get_tailwind_src_path(self):
        app_name = getattr(settings, "TAILWIND_APP_NAME")
        app_label = app_name.split(".")[-1]
        app_path = apps.get_app_config(app_label).path
        return os.path.join(app_path, "static_src")
