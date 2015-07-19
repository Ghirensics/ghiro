from django.apps import AppConfig

from lib.startup import create_auto_upload_dirs

class AnalysesAppConfig(AppConfig):
    name = "analyses"
    verbose_name = "analyses"

    def ready(self):
        # Auto upload dirs.
        create_auto_upload_dirs()