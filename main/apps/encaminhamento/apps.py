from django.apps import AppConfig

class EncaminhamentoConfig(AppConfig):
    name  = 'apps.encaminhamento'
    label = 'apps_encaminhamento'

    def ready(self):
        import apps.encaminhamento.signals
