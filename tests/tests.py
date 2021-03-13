import os
import shutil
import uuid
import json
import pytest

from django.core.management import call_command
from django.apps import apps


@pytest.fixture
def installed_app(settings):
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", app_name)
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    app_label = app_name.split(".")[-1]
    app_path = apps.get_app_config(app_label).path

    yield app_name, app_path

    if os.path.isdir(app_path):
        shutil.rmtree(app_path)


def test_tailwind_init(installed_app):
    _, app_path = installed_app
    assert os.path.isfile(os.path.join(app_path, "apps.py"))
    assert os.path.isfile(os.path.join(app_path, "static_src", "package.json"))
    assert os.path.isfile(os.path.join(app_path, "templates", "base.html"))


def test_tailwind_install(installed_app):
    _, app_path = installed_app

    call_command("tailwind", "install")

    assert os.path.isdir(os.path.join(app_path, "static_src", "node_modules"))

    package_json_path = os.path.join(app_path, "static_src", "package.json")
    with open(package_json_path, "r") as f:
        data = json.load(f)

    tailwindcss = data.get("devDependencies", {}).get("tailwindcss", "")
    assert tailwindcss.startswith("^2.")


def test_tailwind_build(installed_app):
    _, app_path = installed_app

    call_command("tailwind", "install")
    call_command("tailwind", "build")
    assert os.path.isfile(os.path.join(app_path, "static", "css", "styles.css"))
