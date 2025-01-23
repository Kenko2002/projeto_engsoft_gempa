from rest_framework import serializers
from .models import (
    Instituicao,
    UnidadeOrganizacional,
    SetorInstitucional,
    Vaga,
    Funcao,
)


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetorInstitucional
        fields = ['id', 'nome']







class UnidadeOrganizacionalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeOrganizacional
        exclude = ("polymorphic_ctype",)

class UnidadeOrganizacionalReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = UnidadeOrganizacional
        exclude = ("polymorphic_ctype",)

class InstituicaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        exclude = ("polymorphic_ctype",)
        
class InstituicaoReadSerializer(serializers.ModelSerializer):
    unidades_organizacionais = UnidadeOrganizacionalReadSerializer(many=True)
    class Meta:
        depth = 1
        model = Instituicao
        exclude = ("polymorphic_ctype",)


class SetorInstitucionalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetorInstitucional
        exclude = ("polymorphic_ctype",)





class InstituicaoRead2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = ['id', 'nome']  # Inclua os campos que você deseja retornar

class UnidadeOrganizacionalRead2Serializer(serializers.ModelSerializer):
    instituicoes = InstituicaoReadSerializer(many=True)  # Relaciona com Instituicao
    
    class Meta:
        model = UnidadeOrganizacional
        fields = ['id', 'nome', 'hora_abertura', 'hora_fechamento', 'latitude', 'longitude', 'instituicoes']

class SetorInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetorInstitucional
        fields = ['id', 'nome', 'vagas']
        
        
class FuncaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Funcao
        exclude = ("polymorphic_ctype",)
        
        
#=== Serializadores de busca de prestador por vaga na SetorInstitucionalAPIVIEW ===#
from apps.atendimento.models import Execucao,Condicao
from apps.alocacao.models import Alocacao
from apps.socialentity.models import Prestador

class PrestadorSerializerGettedByVaga(serializers.ModelSerializer): # New Prestador Serializer
    class Meta:
        model = Prestador
        fields = ("id","nome")

class ExecucaoReadSerializerGettedByVaga(serializers.ModelSerializer):
    prestador = PrestadorSerializerGettedByVaga()  # Use the PrestadorSerializer

    class Meta:
        model = Execucao
        fields = "__all__" # Include all fields to avoid issues

class CondicaoReadSerializerGettedByVaga(serializers.ModelSerializer):
    class Meta:
        model = Condicao
        fields = (
            "id",
        )

class AlocacaoReadSerializerGettedByVaga(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = (
            "id",
            "vaga",  
        )

class VagaReadSerializer2(serializers.ModelSerializer):
    funcao = FuncaoReadSerializer()
    alocacoes = AlocacaoReadSerializerGettedByVaga(many=True, source="vaga_alocacao")


    class Meta:
        model = Vaga
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for alocacao in data['alocacoes']:
             alocacao_obj=Alocacao.objects.get(pk=alocacao['id'])
             condicoes = Condicao.objects.filter(alocacoes=alocacao_obj).distinct()
             execucoes = Execucao.objects.filter(condicoes__in=condicoes).distinct()
             alocacao['condicoes'] = CondicaoReadSerializerGettedByVaga(condicoes, many=True).data
             alocacao['execucoes'] = ExecucaoReadSerializerGettedByVaga(execucoes, many=True).data
        
        return data
#===============Serializadores de busca de prestador por vaga na SetorInstitucionalAPIVIEW FIM===============#

        
class SetorInstitucionalReadSerializer(serializers.ModelSerializer):
    from apps.socialentity.serializers import ResponsavelReadSerializer
    unidades_organizacionais = UnidadeOrganizacionalRead2Serializer(many=True)
    nome_unidade = serializers.SerializerMethodField()
    nome_referencia = serializers.SerializerMethodField()  # Campo fictício
    responsavel = ResponsavelReadSerializer()
    vagas = VagaReadSerializer2(many=True)
    
    class Meta:
        depth = 2
        model = SetorInstitucional
        fields = ['id', 'nome', 'unidades_organizacionais','responsavel', 'vagas', 'nome_referencia', 'nome_unidade']

    def get_nome_unidade(self, obj):
        if obj.unidades_organizacionais.exists():
            return obj.unidades_organizacionais.first().nome
        return None

    def get_nome_referencia(self, obj):
        # Verifica se há unidades organizacionais associadas
        if obj.unidades_organizacionais.exists():
            unidade = obj.unidades_organizacionais.first()
            
            # Acessa as instituições associadas à unidade
            instituicoes = unidade.instituicoes.all()  # Usando `.all()` para pegar todas as instituições associadas
            
            if instituicoes.exists():
                instituicao_nome = instituicoes.first().nome  # Pegando a primeira instituição
                return f"{instituicao_nome} - {unidade.nome} - {obj.nome}"
        
        return None


















class VagaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        exclude = ("polymorphic_ctype",)

class VagaReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Vaga
        exclude = ("polymorphic_ctype",)


class FuncaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        exclude = ("polymorphic_ctype",)





#=====SERIALIZERS DE FILTRAGEM DE VAGAS DIPONIVEIS POR SETOR====#

class FuncaoVagasDiponiveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        fields = ['id', 'nome']

class VagaVagasDiponiveisSerializer(serializers.ModelSerializer):
    funcao = FuncaoVagasDiponiveisSerializer()

    class Meta:
        model = Vaga
        fields = '__all__'

#=====FIM SERIALIZERS DE FILTRAGEM DE VAGAS DIPONIVEIS POR SETOR====#


#==============AVALIAR PRESTADOR============#

from apps.alocacao.models import DiaCombinado,Alocacao


        
class DiaCombinadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaCombinado
        fields = ['dia_semana', 'horario_entrada', 'horario_saida']

class AvaliacaoSerializer(serializers.ModelSerializer):
    vaga = serializers.PrimaryKeyRelatedField(queryset=Vaga.objects.all())
    diascombinados = DiaCombinadoSerializer(many=True)
    
    class Meta:
        model = Alocacao
        fields = ['data_apresentacao','observacao_avaliacao', 'status', 'vaga', 'diascombinados','vigencia_inicio','vigencia_fim']

    def update(self, instance, validated_data):
        # Atualiza os campos simples
        instance.observacao_avaliacao = validated_data.get('observacao_avaliacao',instance.observacao_avaliacao)
        instance.vigencia_inicio = validated_data.get('vigencia_inicio',instance.vigencia_inicio)
        instance.vigencia_fim = validated_data.get('vigencia_fim',instance.vigencia_fim)
        instance.data_apresentacao = validated_data.get('data_apresentacao', instance.data_apresentacao)
        instance.status = validated_data.get('status', instance.status)
        
        # Atualiza a vaga, se fornecida e confere se o status é recusado.
            #Você não pode trocar a vaga de uma Alocacao, se você recusou ela .-.
        if validated_data.get('status', instance.status) != "RECUSADO":
            vaga_data = validated_data.get('vaga', None)
            if vaga_data:
                instance.vaga = vaga_data

        diascombinados_data = validated_data.pop('diascombinados', [])
        if diascombinados_data:
            # Lista para armazenar os dias combinados que devem ser associados
            novos_dias = []
            
            for dia_data in diascombinados_data:
                dia_combinado= DiaCombinado.objects.create(
                    dia_semana=dia_data['dia_semana'],
                    horario_entrada=dia_data['horario_entrada'],
                    horario_saida=dia_data['horario_saida']
                )
                novos_dias.append(dia_combinado)

            # Atualiza os `ManyToMany` removendo os antigos e associando os novos/existentes
            instance.diascombinados.set(novos_dias)

        # Salva e retorna a instância atualizada
        instance.save()
        return instance

#=============FIM AVALIAR PRESTADOR=========#















##===============CADASTRO DE INSTITUICAO=================##

from rest_framework import serializers
from apps.socialentity.models import Prestador,Endereco,Telefone
from django.shortcuts import get_object_or_404
from .models import Instituicao, UnidadeOrganizacional


##===============fim CADASTRO DE INSTITUICAO=================##






#=====================ENCAMINHAR PARA INSTITUICAO=====================#
from apps.atendimento.models import Condicao

class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = ['prazo_apresentacao', 'vigencia_inicio', 'vigencia_fim', 'status', 'tecnico', 'vaga']

class VagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaga
        fields = ['funcao']  # Assumindo que "funcao" é o único campo relevante para a vaga

class CondicaoAlocacaoSerializer(serializers.Serializer):
    setor_institucional_id = serializers.IntegerField()
    alocacao_id=serializers.IntegerField()

    def create(self, validated_data):
        setor_institucional = SetorInstitucional.objects.get(id=validated_data['setor_institucional_id'])
        
        # Criação da Alocação
        alocacao = Alocacao.objects.get(id=validated_data['alocacao_id'])

        # Criação da Vaga associada à Alocação
        funcao_indefinida, created = Funcao.objects.get_or_create(nome="Indefinido")
        vaga = Vaga.objects.create(funcao=funcao_indefinida)
        
        alocacao.vaga = vaga
        alocacao.save()

        # Adicionando a Vaga ao SetorInstitucional
        setor_institucional.vagas.add(vaga)

        return alocacao
    


#=================FIM ENCAMINHAR PARA INSTITUICAO=====================#



#===============NOVO ENCAMINHAMENTO===================#


class NovoEncaminhamentoSerializer(serializers.Serializer):
    id_condicao = serializers.IntegerField()
    id_tecnico = serializers.IntegerField()
    prazo_apresentacao = serializers.DateField()
    vigencia_inicio = serializers.DateField()
    vigencia_fim = serializers.DateField()

    def validate(self, data):
        if data["vigencia_inicio"] > data["vigencia_fim"]:
            raise serializers.ValidationError(
                {"vigencia_fim": "A data de fim deve ser maior ou igual à data de início."}
            )
        return data

class NovoEncaminhamentoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = ["id", "prazo_apresentacao", "vigencia_inicio", "vigencia_fim", "status", "tecnico"]


#================FIM NOVO ENCAMINHAMENTO===============#


