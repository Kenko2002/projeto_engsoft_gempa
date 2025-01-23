from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

class EnumSexoBiologico(models.TextChoices):
    """"""
    MASCULINO = 'MASCULINO', _('Masculino')
    FEMININO = 'FEMININO', _('Feminino')
    INTERSEXO = 'INTERSEXO', _('Intersexo')


class EnumPrestadorNaturalidade(models.TextChoices):
    """"""
    BRASILEIRO = 'BRASILEIRO', _('Brasileiro')
    OUTRO = 'OUTRO', _('Outro')


class EnumPrestadorCor(models.TextChoices):
    """"""
    BRANCO = 'BRANCO', _('Branco')
    PRETO = 'PRETO', _('Preto')
    AMARELO = 'AMARELO', _('Amarelo')
    PARDO = 'PARDO', _('Pardo')
    INDIGENA = 'INDIGENA', _('Indígena')


class EnumPrestadorReligiao(models.TextChoices):
    """"""
    CATOLICO = 'CATOLICO', _('Católico')
    EVANGELICO = 'EVANGELICO', _('Evangélico')
    UMBANDISTA = 'UMBANDISTA', _('Umbandista')
    JUDAISMO = 'JUDAISMO', _('Judaísmo')
    PENTECOSTAIS = 'PENTECOSTAIS', _('Pentecostais')
    NEOPENTECOSTAIS = 'NEOPENTECOSTAIS', _('Neopentecostais')
    EVANGELICOS_DE_MISSAO = 'EVANGELICOS_DE_MISSAO', _('Evangélicos de missão')
    ESPIRITA = 'ESPIRITA', _('Espírita')
    CANDOMBLE = 'CANDOMBLE', _('Candomblé')
    ATEU = 'ATEU', _('Ateu')



class Endereco(models.Model):
    """Classe para representar um endereço."""
    logradouro = models.CharField(max_length=300, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    bairro = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


class Telefone(models.Model):
    """Classe para representar um telefone."""
    numero = models.CharField(max_length=20, null=False, blank=False)
    ddd = models.CharField(max_length=20, null=False, blank=False)
    
    def __str__(self):
        return f"+{self.ddd} {self.numero}"
    
class EntidadeSocial(PolymorphicModel, models.Model):
    """"""
    nome = models.CharField(max_length=300, null=True, blank=True)
    identificacao = models.CharField(max_length=300, null=True, blank=True)
    ativo = models.BooleanField(null=True, blank=True)
    email_contato = models.CharField(max_length=300, null=True, blank=True)
    
    enderecos = models.ManyToManyField(Endereco, blank=True)
    telefones = models.ManyToManyField(Telefone, blank=True)

    class Meta:
        abstract = True 

    def __str__(self):
        return self.nome if self.nome else "Entidade Social sem nome"

from django.contrib.auth.models import User
class Usuario(EntidadeSocial,PolymorphicModel, models.Model):
    """"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.user if self.user else "Usuário sem nome"


class Prestador(EntidadeSocial):
    """"""
    foto = models.TextField(null=True, blank=True)
    rg = models.CharField(max_length=300, null=True, blank=True)
    nome_social = models.CharField(max_length=300, null=True, blank=True)
    escolaridade = models.CharField(max_length=300, null=True, blank=True)
    situacao_economica = models.CharField(max_length=300, null=True, blank=True)
    descricao_avaliacao_psicosocial = models.CharField(max_length=300, null=True, blank=True)

    naturalidade = models.CharField(
        max_length=10, choices=EnumPrestadorNaturalidade.choices, default=EnumPrestadorNaturalidade.BRASILEIRO
    )
    cor = models.CharField(
        max_length=8, choices=EnumPrestadorCor.choices, default=EnumPrestadorCor.BRANCO
    )
    religiao = models.CharField(
        max_length=30, choices=EnumPrestadorReligiao.choices, default=EnumPrestadorReligiao.CATOLICO
    )
    sexo_biologico = models.CharField(
        max_length=9, choices=EnumSexoBiologico.choices, default=EnumSexoBiologico.MASCULINO
    )

    class Meta:
        db_table = 'prestador'

    def __str__(self):
        return self.nome if self.nome else f"Prestador ({self.nome})"


class Tecnico(Usuario):
    """"""

    class Meta:
        db_table = 'tecnico'

    def __str__(self):
        return f"Técnico: {self.user}" if self.user else "Técnico sem nome"


class Fiscal(Usuario):
    """"""

    class Meta:
        db_table = 'fiscal'

    def __str__(self):
        return f"Fiscal: {self.user}" if self.user else "Fiscal sem nome"


class Coordenador(Usuario):
    """"""

    class Meta:
        db_table = 'coordenador'

    def __str__(self):
        return f"Coordenador: {self.user}" if self.user else "Coordenador sem nome"


class Responsavel(Usuario):
    """"""
    
    class Meta:
        db_table = 'responsavel'

    def __str__(self):
        return f"Responsável: {self.user}" if self.user else "Responsável sem nome"
