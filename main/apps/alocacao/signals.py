from .models import Alocacao
from django.db.models.signals import (
    pre_init,   post_init,
    pre_save,   post_save,
    pre_delete, post_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.contrib.auth.models import Group

## Signals from Alocacao
@receiver(pre_init, sender=Alocacao)
def pre_init_alocacao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Alocacao)
def post_init_alocacao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Alocacao)
def pre_save_alocacao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Alocacao)
def post_save_alocacao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Alocacao)
def pre_delete_alocacao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Alocacao)
def post_delete_alocacao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Alocacao)
def m2m_changed_alocacao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass

