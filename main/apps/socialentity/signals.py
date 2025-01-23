from .models import EntidadeSocial, Prestador, Tecnico, Fiscal, Coordenador, Responsavel
from django.db.models.signals import (
    pre_init,   post_init,
    pre_save,   post_save,
    pre_delete, post_delete,
    m2m_changed
)
from django.dispatch import receiver
from django.contrib.auth.models import Group

## Signals from EntidadeSocial
@receiver(pre_init, sender=EntidadeSocial)
def pre_init_entidadesocial(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=EntidadeSocial)
def post_init_entidadesocial(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=EntidadeSocial)
def pre_save_entidadesocial(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=EntidadeSocial)
def post_save_entidadesocial(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=EntidadeSocial)
def pre_delete_entidadesocial(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=EntidadeSocial)
def post_delete_entidadesocial(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=EntidadeSocial)
def m2m_changed_entidadesocial(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass





## Signals from Prestador
@receiver(pre_init, sender=Prestador)
def pre_init_prestador(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Prestador)
def post_init_prestador(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Prestador)
def pre_save_prestador(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Prestador)
def post_save_prestador(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Prestador)
def pre_delete_prestador(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Prestador)
def post_delete_prestador(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Prestador)
def m2m_changed_prestador(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Tecnico
@receiver(pre_init, sender=Tecnico)
def pre_init_tecnico(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Tecnico)
def post_init_tecnico(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Tecnico)
def pre_save_tecnico(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Tecnico)
def post_save_tecnico(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Tecnico)
def pre_delete_tecnico(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Tecnico)
def post_delete_tecnico(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Tecnico)
def m2m_changed_tecnico(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Fiscal
@receiver(pre_init, sender=Fiscal)
def pre_init_fiscal(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Fiscal)
def post_init_fiscal(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Fiscal)
def pre_save_fiscal(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Fiscal)
def post_save_fiscal(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Fiscal)
def pre_delete_fiscal(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Fiscal)
def post_delete_fiscal(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Fiscal)
def m2m_changed_fiscal(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Coordenador
@receiver(pre_init, sender=Coordenador)
def pre_init_coordenador(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Coordenador)
def post_init_coordenador(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Coordenador)
def pre_save_coordenador(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Coordenador)
def post_save_coordenador(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Coordenador)
def pre_delete_coordenador(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Coordenador)
def post_delete_coordenador(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Coordenador)
def m2m_changed_coordenador(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass


## Signals from Responsavel
@receiver(pre_init, sender=Responsavel)
def pre_init_responsavel(sender, *args, **kwargs):
    pass

@receiver(post_init, sender=Responsavel)
def post_init_responsavel(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=Responsavel)
def pre_save_responsavel(sender, instance, raw, using, update_fields, **kwargs):
    pass

@receiver(post_save, sender=Responsavel)
def post_save_responsavel(sender, instance, created, raw, using, update_fields, **kwargs):
    pass

@receiver(pre_delete, sender=Responsavel)
def pre_delete_responsavel(sender, instance, using, **kwargs):
    pass

@receiver(post_delete, sender=Responsavel)
def post_delete_responsavel(sender, instance, using, **kwargs):
    pass

@receiver(m2m_changed, sender=Responsavel)
def m2m_changed_responsavel(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    pass

