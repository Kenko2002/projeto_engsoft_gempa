from .models import Instituicao, UnidadeOrganizacional, SetorInstitucional, Vaga, Funcao
from django.db.models.signals import (
    pre_init,   post_init,
    pre_save,   post_save,
    pre_delete, post_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.contrib.auth.models import Group

## Signals from Instituicao
@receiver(pre_init, sender=Instituicao)
def pre_init_instituicao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Instituicao)
def post_init_instituicao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Instituicao)
def pre_save_instituicao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Instituicao)
def post_save_instituicao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Instituicao)
def pre_delete_instituicao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Instituicao)
def post_delete_instituicao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Instituicao)
def m2m_changed_instituicao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from UnidadeOrganizacional
@receiver(pre_init, sender=UnidadeOrganizacional)
def pre_init_unidadeorganizacional(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=UnidadeOrganizacional)
def post_init_unidadeorganizacional(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=UnidadeOrganizacional)
def pre_save_unidadeorganizacional(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=UnidadeOrganizacional)
def post_save_unidadeorganizacional(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=UnidadeOrganizacional)
def pre_delete_unidadeorganizacional(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=UnidadeOrganizacional)
def post_delete_unidadeorganizacional(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=UnidadeOrganizacional)
def m2m_changed_unidadeorganizacional(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from SetorInstitucional
@receiver(pre_init, sender=SetorInstitucional)
def pre_init_setorinstitucional(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=SetorInstitucional)
def post_init_setorinstitucional(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=SetorInstitucional)
def pre_save_setorinstitucional(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=SetorInstitucional)
def post_save_setorinstitucional(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=SetorInstitucional)
def pre_delete_setorinstitucional(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=SetorInstitucional)
def post_delete_setorinstitucional(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=SetorInstitucional)
def m2m_changed_setorinstitucional(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Vaga
@receiver(pre_init, sender=Vaga)
def pre_init_vaga(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Vaga)
def post_init_vaga(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Vaga)
def pre_save_vaga(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Vaga)
def post_save_vaga(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Vaga)
def pre_delete_vaga(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Vaga)
def post_delete_vaga(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Vaga)
def m2m_changed_vaga(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Funcao
@receiver(pre_init, sender=Funcao)
def pre_init_funcao(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Funcao)
def post_init_funcao(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Funcao)
def pre_save_funcao(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Funcao)
def post_save_funcao(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Funcao)
def pre_delete_funcao(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Funcao)
def post_delete_funcao(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Funcao)
def m2m_changed_funcao(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass

