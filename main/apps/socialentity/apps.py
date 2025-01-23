from django.apps import AppConfig

class SocialEntityConfig(AppConfig):
    name  = 'apps.socialentity'
    label = 'apps_socialentity'

    def ready(self):
        import apps.socialentity.signals
