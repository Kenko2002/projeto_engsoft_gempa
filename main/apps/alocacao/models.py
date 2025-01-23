from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from apps.socialentity.models import Tecnico
from apps.encaminhamento.models import Vaga
from django.utils.timezone import localtime

from django.utils.timezone import now


class EnumStatusAlocacao(models.TextChoices):
    """"""
    AGUARDANDO_ENTREVISTA = 'AGUARDANDO_ENTREVISTA', _('Aguardando entrevista')
    CUMPRINDO = 'CUMPRINDO', _('Cumprindo')
    RECUSADO = 'RECUSADO', _('Recusado')
    INATIVO = 'INATIVO', _('Inativo')
    IRREGULAR = 'IRREGULAR', _('Irregular')

class EnumDiaDaSemana(models.TextChoices):
    """"""
    SEGUNDA_FEIRA = 'SEGUNDA_FEIRA', _('Segunda feira')
    TERCA_FEIRA = 'TERCA_FEIRA', _('Terca feira')
    QUARTA_FEIRA = 'QUARTA_FEIRA', _('Quarta feira')
    QUINTA_FEIRA = 'QUINTA_FEIRA', _('Quinta feira')
    SEXTA_FEIRA = 'SEXTA_FEIRA', _('Sexta feira')
    SABADO = 'SABADO', _('Sabado')
    DOMINGO = 'DOMINGO', _('Domingo')
    QUALQUER = 'QUALQUER', _('Qualquer')


class Alocacao(PolymorphicModel, models.Model):
    """"""
    prazo_apresentacao = models.DateField(null=True, blank=True)
    data_apresentacao = models.DateField(null=True,  default=None,blank=True)
    vigencia_inicio = models.DateField(null=True, blank=True)
    vigencia_fim = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=30, 
        choices=EnumStatusAlocacao.choices, 
        default=EnumStatusAlocacao.AGUARDANDO_ENTREVISTA
    )
    
    observacao_avaliacao=models.CharField(max_length=300, null=True, blank=True)
    
    

    tecnico = models.ForeignKey(
        'apps_socialentity.Tecnico', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="tecnico_%(class)s"
    )
    vaga = models.ForeignKey(
        'apps_encaminhamento.Vaga', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="vaga_%(class)s"
    )
    
    
    presencas = models.ManyToManyField(
        'Presenca',
        blank=True,
        related_name='presencas'
    )
    
    diascombinados = models.ManyToManyField(
        'DiaCombinado',
        blank=True,
        related_name='diascombinados'
    )

    class Meta:
        db_table = 'alocacao'

    def __str__(self):
        tecnico_nome = self.tecnico.user if self.tecnico and self.tecnico.user else "Técnico desconhecido"
        vaga_titulo = self.vaga.titulo if self.vaga and hasattr(self.vaga, 'titulo') else "Vaga desconhecida"
        return f"Alocação: {tecnico_nome} - {vaga_titulo} ({self.get_status_display()})"




class Presenca(PolymorphicModel, models.Model):
    """"""
    from datetime import timedelta
    
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)
    observacao_checkin = models.CharField(max_length=300, null=True, blank=True)
    observacao_checkout = models.CharField(max_length=300, null=True, blank=True)
    tempo_intervalo=models.DurationField(default=timedelta(0),null=True, blank=True)
    
    hora_cadastro_checkin = models.DateTimeField(null=True, blank=True)
    hora_cadastro_checkout = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'presenca'

    def __str__(self):
        checkin = localtime(self.checkin) if self.checkin else None
        checkout = localtime(self.checkout) if self.checkout else None

        formatted_checkin = checkin.strftime('%d/%m/%Y %H:%M:%S') if checkin else "Sem check-in"
        formatted_checkout = checkout.strftime('%d/%m/%Y %H:%M:%S') if checkout else "Sem check-out"

        return f"{formatted_checkin} - {formatted_checkout}"


class DiaCombinado(PolymorphicModel, models.Model):
    """"""
    dia_semana = models.CharField(
        max_length=30, 
        choices=EnumDiaDaSemana.choices,
        default=EnumDiaDaSemana.SEGUNDA_FEIRA
    )
    horario_entrada=models.TimeField(null=True, blank=True)
    horario_saida=models.TimeField(null=True, blank=True)
    
    

    
    class Meta:
        db_table = 'diacombinado'

    def __str__(self):
        dia=self.dia_semana
        entrada=self.horario_entrada
        saida=self.horario_saida
        return f"{dia}: {entrada}/{saida}"