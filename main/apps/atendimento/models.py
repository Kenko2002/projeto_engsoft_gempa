from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from apps.socialentity.models import Tecnico, Prestador
from apps.alocacao.models import Alocacao
from datetime import timedelta

class EnumAtendimentoStatus(models.TextChoices):
    """"""
    AGENDADO = 'AGENDADO', _('Agendado')
    CANCELADO = 'CANCELADO', _('Cancelado')
    EXPIRADO = 'EXPIRADO', _('Expirado')
    CONCLUIDO = 'CONCLUIDO', _('Concluido')

class EnumPrestacaoStatus(models.TextChoices):
    """"""
    ATIVA = 'ATIVA', _('Ativa')
    SUSPENSA = 'SUSPENSA', _('Suspensa')
    CONCLUIDA = 'CONCLUIDA', _('Concluida')
    INATIVA = 'INATIVA', _('Inativa')

class EnumTipoProcessual(models.TextChoices):
    """"""
    PRD = 'PRD', _('Prd')
    ANPP = 'ANPP', _('Anpp')


class Atendimento(PolymorphicModel, models.Model):
    """"""

    horario = models.DateTimeField(blank=True)
    motivo = models.CharField(max_length=300, null=True, blank=True)
    observacao = models.CharField(max_length=300, null=True, blank=True)
    justificativa_cancelamento = models.CharField(max_length=300, null=True, blank=True)

    status = models.CharField(
        max_length=9, 
        choices=EnumAtendimentoStatus.choices, 
        default=EnumAtendimentoStatus.AGENDADO
    )

    tecnico = models.ForeignKey(
        'apps_socialentity.Tecnico', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="tecnico_%(class)s"
    )
    prestador = models.ForeignKey(
        'apps_socialentity.Prestador', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="prestador_%(class)s"
    )

    class Meta:
        db_table = 'atendimento'

    def __str__(self):
        return f"Atendimento: {self.horario} - {self.get_status_display()}"


class Observacao(PolymorphicModel, models.Model):
    """"""

    texto = models.CharField(max_length=300, null=True, blank=True)
    link_arquivo = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'observacao'

    def __str__(self):
        return f"Observação: {self.texto[:50]}{'...' if len(self.texto) > 50 else ''}"


class Execucao(PolymorphicModel, models.Model):
    """"""

    num_processo = models.CharField(max_length=300, null=True, blank=True)
    rji = models.CharField(max_length=300, null=True, blank=True)

    status = models.CharField(
        max_length=9, 
        choices=EnumPrestacaoStatus.choices, 
        default=EnumPrestacaoStatus.ATIVA
    )

    prestador = models.ForeignKey(
        'apps_socialentity.Prestador', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name="prestador_%(class)s"
    )

    observacoes = models.ManyToManyField(
        'Observacao', 
        blank=True,
        related_name="observacoes"
    )
    condicoes = models.ManyToManyField(
        'Condicao', 
        blank=True,
        related_name="condicoes"
    )

    class Meta:
        db_table = 'execucao'

    def __str__(self):
        return f"Execução: {self.num_processo or 'N/A'} - {self.get_status_display()}"





    class Meta:
        db_table = 'execucao'

class Condicao(PolymorphicModel, models.Model):
    """"""

    ch_cumprida_anterior_cadastro= models.DurationField(null=True ,blank=True,default=timedelta(0))
    
    #atualmente esse atributo nao é usado pra nada, mas no futuro vamos usar ele para não precisarmos calcular
    #o quantitativo de horas cumpridas totais toda vez que alguém precisar dessa info.
    horas_cumpridas_totais = models.DurationField(null=True ,blank=True)
    flexivel_dia = models.BooleanField(null=True, blank=True)
    flexivel_horario = models.BooleanField(null=True, blank=True)
    horas_minimas = models.IntegerField(null=True, blank=True)
    horas_maximas = models.IntegerField(null=True, blank=True)
    periodo_dias = models.IntegerField(null=True, blank=True)

    tipo_processual = models.CharField(
        max_length=4, 
        choices=EnumTipoProcessual.choices, 
        default=EnumTipoProcessual.PRD
    )

    historico_carga_horaria = models.ManyToManyField(
        'HistoricoCargaHoraria', 
        blank=True,
        related_name="historico_carga_horaria"
    )
    alocacoes = models.ManyToManyField(
        'apps_alocacao.Alocacao', 
        blank=True,
        related_name="alocacoes"
    )

    class Meta:
        db_table = 'condicao'

    def __str__(self):
        return f"Condição: {self.get_tipo_processual_display()} - {self.horas_minimas}h min / {self.horas_maximas}h max"


class HistoricoCargaHoraria(PolymorphicModel, models.Model):
    """"""

    carga_horaria_total = models.IntegerField(null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'historicocargahoraria'

    def __str__(self):
        return f"Histórico de Carga: {self.carga_horaria_total or 0}h - Início: {self.data_inicio or 'N/A'}"
