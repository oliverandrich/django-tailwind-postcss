import json
import shutil
import uuid
from pathlib import Path

import pytest
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.fixture
def installed_app(settings):
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    call_command("tailwind", "init", app_name)
    settings.INSTALLED_APPS += [app_name]
    settings.TAILWIND_APP_NAME = app_name

    app_label = app_name.split(".")[-1]
    app_path = Path(apps.get_app_config(app_label).path)

    yield app_name, app_path

    if app_path.is_dir():
        shutil.rmtree(app_path)


def test_tailwind_init(installed_app):
    _, app_path = installed_app
    for fname in [
        "apps.py",
        "package.json",
        "tailwind.config.js",
        "postcss.config.js",
        "templates/base.html",
    ]:
        assert (app_path / fname).is_file()


def test_tailwind_init_with_invalid_appname():
    with pytest.raises(CommandError):
        call_command("tailwind", "init", "invalid-appname")


def test_validate_app_with_missing_tailwind_app_name_setting(installed_app, settings):
    del settings.TAILWIND_APP_NAME
    with pytest.raises(CommandError) as excinfo:
        call_command("tailwind", "install")
    assert "TAILWIND_APP_NAME isn't set in settings.py" in str(excinfo.value)


def test_validate_app_with_missing_installed_app(installed_app, settings):
    app_name, _ = installed_app
    settings.INSTALLED_APPS = [app for app in settings.INSTALLED_APPS if app != app_name]
    with pytest.raises(CommandError) as excinfo:
        call_command("tailwind", "install")
    assert f"{app_name} is not in INSTALLED_APPS" in str(excinfo.value)


def test_validate_app_with_missing_tailwind_config_js(installed_app, settings):
    app_name, app_path = installed_app
    (app_path / "tailwind.config.js").unlink()
    with pytest.raises(CommandError) as excinfo:
        call_command("tailwind", "install")
    assert f"{app_name} isn't a Tailwind app" in str(excinfo.value)


def test_tailwind_install(installed_app):
    _, app_path = installed_app

    call_command("tailwind", "install")

    assert (app_path / "node_modules").is_dir()

    package_json_path = app_path / "package.json"
    with open(package_json_path, "r") as f:
        data = json.load(f)

    tailwindcss = data.get("devDependencies", {}).get("tailwindcss", "")
    assert tailwindcss.startswith("^2.")


def test_tailwind_install_with_broken_npm(installed_app, settings):
    settings.NPM_BIN_PATH = "npm2"
    with pytest.raises(CommandError) as excinfo:
        call_command("tailwind", "install")
    assert "It looks like node.js and/or npm is not installed" in str(excinfo.value)


def test_tailwind_build(installed_app):
    _, app_path = installed_app

    call_command("tailwind", "install")
    call_command("tailwind", "build")
    assert (app_path / "static" / "css" / "styles.css").is_file()


def test_tailwind_nonexisting_subcommand(installed_app):
    with pytest.raises(Exception) as excinfo:
        call_command("tailwind", "i_do_not_exist")
    assert "Subcommand i_do_not_exist doesn't exist" in str(excinfo.value)


def test_tailwind_check_updates(installed_app):
    call_command("tailwind", "check-updates")


def test_tailwind_update(installed_app):
    call_command("tailwind", "update")
