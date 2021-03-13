import os
import shutil
import uuid
import json

from django.core.management import call_command
from django.test import SimpleTestCase


class CliTestCast(SimpleTestCase):
    def setUp(self):
        self.app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    def tearDown(self):
        try:
            with self.modify_settings(INSTALLED_APPS={"append": self.app_name}):
                theme_app_dir = self._get_app_path()
                if os.path.isdir(theme_app_dir):
                    shutil.rmtree(theme_app_dir)
        except ModuleNotFoundError:
            pass

    def test_tailwind_init(self):
        call_command("tailwind", "init", self.app_name)

        with self.modify_settings(INSTALLED_APPS={"append": self.app_name}):
            app_path = self._get_app_path()

        self.assertTrue(os.path.isfile(os.path.join(app_path, "apps.py")))
        self.assertTrue(os.path.isfile(os.path.join(app_path, "static_src", "package.json")))
        self.assertTrue(os.path.isfile(os.path.join(app_path, "templates", "base.html")))

    def test_tailwind_install(self):
        call_command("tailwind", "init", self.app_name)

        with self.modify_settings(INSTALLED_APPS={"append": self.app_name}):
            app_path = self._get_app_path()
            with self.settings(TAILWIND_APP_NAME=self.app_name):
                call_command("tailwind", "install")

        self.assertTrue(os.path.isdir(os.path.join(app_path, "static_src", "node_modules")))

        with self.modify_settings(INSTALLED_APPS={"append": self.app_name}):
            data = self._get_package_json_contents()
            tailwindcss = data.get("devDependencies", {}).get("tailwindcss", "")
            self.assertTrue(tailwindcss.startswith("^2."))

    def test_tailwind_build(self):
        call_command("tailwind", "init", self.app_name)

        with self.modify_settings(INSTALLED_APPS={"append": self.app_name}):
            app_path = self._get_app_path()
            with self.settings(TAILWIND_APP_NAME=self.app_name):
                call_command("tailwind", "install")
                call_command("tailwind", "build")

        self.assertTrue(os.path.isfile(os.path.join(app_path, "static", "css", "styles.css")))

    def _get_app_path(self):
        from django.apps import apps

        app_label = self.app_name.split(".")[-1]
        return apps.get_app_config(app_label).path

    def _get_package_json_contents(self):
        package_json_path = os.path.join(self._get_app_path(), "static_src", "package.json")
        with open(package_json_path, "r") as f:
            return json.load(f)
