from django.apps import AppConfig

class AtendimentoConfig(AppConfig):
    name  = 'apps.atendimento'
    label = 'apps_atendimento'

    def ready(self):
        import apps.atendimento.signals
