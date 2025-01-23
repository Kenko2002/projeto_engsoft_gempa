from django.apps import AppConfig

class AlocacaoConfig(AppConfig):
    name  = 'apps.alocacao'
    label = 'apps_alocacao'

    def ready(self):
        import apps.alocacao.signals
