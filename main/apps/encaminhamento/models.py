from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from apps.socialentity.models import EntidadeSocial
from apps.socialentity.models import Responsavel


class Instituicao(EntidadeSocial):
    """"""

    unidades_organizacionais = models.ManyToManyField(
        'UnidadeOrganizacional',
        blank=True,
        related_name='instituicoes'
    )
    
    class Meta:
        
        db_table = 'instituicao'

    def __str__(self):
        return self.nome if hasattr(self, 'nome') and self.nome else "Instituição sem nome"


class UnidadeOrganizacional(EntidadeSocial):
    """"""

    hora_abertura = models.TimeField(blank=True)
    hora_fechamento = models.TimeField(blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    setores_institucionais = models.ManyToManyField(
        'SetorInstitucional',
        blank=True,
        related_name='unidades_organizacionais'
    )

    class Meta:
        
        db_table = 'unidadeorganizacional'

    def __str__(self):
        return self.nome if hasattr(self, 'nome') and self.nome else "Unidade Organizacional sem nome"


class SetorInstitucional(PolymorphicModel, models.Model):
    """"""
    responsavel = models.OneToOneField(
        Responsavel, 
        on_delete=models.CASCADE, 
        related_name='setor_institucional',
        null=True, 
        blank=True
    )
    nome = models.CharField(max_length=300, null=True, blank=True)
    vagas = models.ManyToManyField(
            'Vaga',
            blank=True,
            related_name='setores_institucionais'
        )
    
    class Meta:
        
        db_table = 'setorinstitucional'

    def __str__(self):
        return self.nome if self.nome else "Setor Institucional sem nome"


class Vaga(PolymorphicModel, models.Model):
    """"""

    
    funcao = models.ForeignKey('Funcao', blank=True, null=True, on_delete=models.CASCADE, related_name="funcao_%(class)s")

    class Meta:
        
        db_table = 'vaga'

    def __str__(self):
        nome_funcao = self.funcao.nome if self.funcao else "Função desconhecida"
        return f"Vaga ({nome_funcao})"


class Funcao(PolymorphicModel, models.Model):
    """"""

    nome = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        
        db_table = 'funcao'

    def __str__(self):
        return self.nome if self.nome else "Função sem nome"
