from .models import Atendimento, Observacao, Execucao, Condicao, HistoricoCargaHoraria
from django.db.models.signals import (
    pre_init,   post_init,
    pre_save,   post_save,
    pre_delete, post_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.contrib.auth.models import Group

## Signals from Atendimento
@receiver(pre_init, sender=Atendimento)
def pre_init_atendimento(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Atendimento)
def post_init_atendimento(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Atendimento)
def pre_save_atendimento(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Atendimento)
def post_save_atendimento(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Atendimento)
def pre_delete_atendimento(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Atendimento)
def post_delete_atendimento(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Atendimento)
def m2m_changed_atendimento(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Observacao
@receiver(pre_init, sender=Observacao)
def pre_init_observacao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Observacao)
def post_init_observacao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Observacao)
def pre_save_observacao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Observacao)
def post_save_observacao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Observacao)
def pre_delete_observacao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Observacao)
def post_delete_observacao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Observacao)
def m2m_changed_observacao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Execucao
@receiver(pre_init, sender=Execucao)
def pre_init_execucao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Execucao)
def post_init_execucao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Execucao)
def pre_save_execucao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Execucao)
def post_save_execucao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Execucao)
def pre_delete_execucao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Execucao)
def post_delete_execucao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Execucao)
def m2m_changed_execucao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Condicao
@receiver(pre_init, sender=Condicao)
def pre_init_condicao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Condicao)
def post_init_condicao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Condicao)
def pre_save_condicao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Condicao)
def post_save_condicao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Condicao)
def pre_delete_condicao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Condicao)
def post_delete_condicao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Condicao)
def m2m_changed_condicao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from HistoricoCargaHoraria
@receiver(pre_init, sender=HistoricoCargaHoraria)
def pre_init_historicocargahoraria(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=HistoricoCargaHoraria)
def post_init_historicocargahoraria(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=HistoricoCargaHoraria)
def pre_save_historicocargahoraria(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=HistoricoCargaHoraria)
def post_save_historicocargahoraria(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=HistoricoCargaHoraria)
def pre_delete_historicocargahoraria(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=HistoricoCargaHoraria)
def post_delete_historicocargahoraria(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=HistoricoCargaHoraria)
def m2m_changed_historicocargahoraria(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass

