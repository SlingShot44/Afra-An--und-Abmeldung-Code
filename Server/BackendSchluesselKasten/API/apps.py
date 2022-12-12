from django.apps import AppConfig


class APIConfig(AppConfig):
    name = 'API'

    def ready(self):
        import API.signals
