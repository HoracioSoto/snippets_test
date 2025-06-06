from __future__ import unicode_literals

from django.apps import AppConfig


class SnippetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "snippets"

    def ready(self):
        import snippets.signals
