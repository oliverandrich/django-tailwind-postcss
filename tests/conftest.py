import shutil
import uuid
from pathlib import Path

import pytest
from django.apps import apps
from django.core.management import call_command


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
