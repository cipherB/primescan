from django.apps import AppConfig
import os


class AppsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps"


def get_app_names():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    apps_directory = current_directory
    app_names = [
        "apps." + app_name
        for app_name in os.listdir(apps_directory)
        if os.path.isdir(os.path.join(apps_directory, app_name))
        and app_name not in ["utils", "migrations"]
    ]
    return app_names
