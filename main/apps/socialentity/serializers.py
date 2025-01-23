from rest_framework import serializers
from .models import (
    EntidadeSocial,
    Prestador,
    Tecnico,
    Fiscal,
    Coordenador,
    Responsavel,
)


from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Prestador,Endereco,Telefone
from apps.atendimento.models import Execucao, Condicao
from apps.alocacao.models import Alocacao
from apps.atendimento.models import HistoricoCargaHoraria
from datetime import datetime

#SERIALIZADORES RELATIVOS AO EVENTO INCLUIR PRESTADOR, QUE INCLUEM OS DADOS DE NUM_PROCESSO E TIPO PROCESSUAL.#
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = ['ddd', 'numero']

class PrimeiraEntrevistaIncluirPrestadorAPIViewSerializer(serializers.ModelSerializer):
    num_processo = serializers.CharField(max_length=300)
    rji=serializers.CharField(max_length=300)
    tecnico_id=serializers.IntegerField()
    prazo_apresentacao = serializers.DateField()
    
    vigencia_inicio = serializers.DateField()
    vigencia_fim = serializers.DateField()
    carga_horaria_total= serializers.IntegerField()
    
    
    tipo_processual = serializers.CharField(max_length=4)
    
    flexivel_dia= serializers.BooleanField(required=True)
    flexivel_horario=serializers.BooleanField(required=True)
    horas_minimas=serializers.IntegerField()
    horas_maximas=serializers.IntegerField()
    periodo_dias=serializers.IntegerField()
    
    
    
    
    enderecos = EnderecoSerializer(many=True)
    telefones = TelefoneSerializer(many=True)
    
    prestador_id = serializers.IntegerField(required=False, allow_null=True)  # ID do prestador, caso exista

    class Meta:
        model = Prestador
        fields = [
            'prestador_id','nome', 'identificacao','enderecos', 'telefones','email_contato' ,'ativo', 'foto', 'rg', 'nome_social', 'escolaridade', 
            'situacao_economica',"carga_horaria_total", 'descricao_avaliacao_psicosocial', 'num_processo', 'rji',
            'tipo_processual','flexivel_dia','flexivel_horario','horas_minimas','horas_maximas','periodo_dias', 'naturalidade', 'cor', 'religiao', 'sexo_biologico','prazo_apresentacao','tecnico_id','vigencia_inicio','vigencia_fim'
        ]

    def create(self, validated_data):
        # Extração de campos adicionais
        prestador_id = validated_data.pop('prestador_id', None)
        num_processo = validated_data.pop('num_processo')
        tipo_processual = validated_data.pop('tipo_processual')
        
        flexivel_dia= validated_data.pop('flexivel_dia')
        flexivel_horario= validated_data.pop('flexivel_horario')
        horas_minimas= validated_data.pop('horas_minimas')
        horas_maximas= validated_data.pop('horas_maximas')
        periodo_dias= validated_data.pop('periodo_dias')
        
        rji = validated_data.pop("rji")
        prazo_apresentacao = validated_data.pop("prazo_apresentacao")
        tecnico_id = validated_data.pop("tecnico_id")
        vigencia_inicio = validated_data.pop("vigencia_inicio")
        vigencia_fim = validated_data.pop("vigencia_fim")
        carga_horaria_total=validated_data.pop("carga_horaria_total")
        enderecos_data = validated_data.pop('enderecos', [])
        telefones_data = validated_data.pop('telefones', [])

        try:
            tecnico = Tecnico.objects.get(id=tecnico_id)
        except Tecnico.DoesNotExist:
            raise serializers.ValidationError({"tecnico_id": "Técnico não encontrado."})

        if prestador_id:
            try:
                prestador = Prestador.objects.get(id=prestador_id)
                # Atualiza o prestador com os dados fornecidos
                for field, value in validated_data.items():
                    setattr(prestador, field, value)
                prestador.save()  # Salva as mudanças
            except Prestador.DoesNotExist:
                raise serializers.ValidationError({"prestador_id": "Prestador não encontrado."})
        else:
            # Caso contrário, cria um novo prestador
            prestador = Prestador.objects.create(**validated_data)

        
        # Criação e associação de endereços
        for endereco_data in enderecos_data:
            endereco = Endereco.objects.create(**endereco_data)
            prestador.enderecos.add(endereco)

        # Criação e associação de telefones
        for telefone_data in telefones_data:
            telefone = Telefone.objects.create(**telefone_data)
            prestador.telefones.add(telefone)
            
        execucao = Execucao.objects.create(prestador=prestador, num_processo=num_processo, rji=rji)
        condicao = Condicao.objects.create(tipo_processual=tipo_processual,
                                           flexivel_dia=flexivel_dia,
                                           flexivel_horario=flexivel_horario,
                                           horas_minimas=horas_minimas,
                                           horas_maximas=horas_maximas,
                                           periodo_dias=periodo_dias
                                           )
        
        
        execucao.condicoes.add(condicao)
        
        carga_horaria= HistoricoCargaHoraria.objects.create(carga_horaria_total=carga_horaria_total,data_inicio=datetime.now())
        condicao.historico_carga_horaria.add(carga_horaria)
        
        alocacao = Alocacao.objects.create(
            prazo_apresentacao=prazo_apresentacao,
            tecnico=tecnico,
            vigencia_inicio=vigencia_inicio,
            vigencia_fim=vigencia_fim
        )
        condicao.alocacoes.add(alocacao)

        # Retorno dos objetos criados
        return prestador, execucao, condicao, alocacao ,carga_horaria


    def to_representation(self, instance):
        # Obtém a representação padrão
        representation = super().to_representation(instance)
        
        # Adiciona os campos extras
        representation['num_processo'] = getattr(instance, 'num_processo', None)
        
        
        representation['tipo_processual'] = getattr(instance, 'tipo_processual', None)
        
        representation['flexivel_dia'] = getattr(instance, 'flexivel_dia', None)
        representation['flexivel_horario'] = getattr(instance, 'flexivel_horario', None)
        representation['horas_minimas'] = getattr(instance, 'horas_minimas', None)
        representation['horas_maximas'] = getattr(instance, 'horas_maximas', None)
        representation['periodo_dias'] = getattr(instance, 'periodo_dias', None)
        
        
        representation['rji'] = getattr(instance, 'rji', None)
        representation['prazo_apresentacao'] = getattr(instance, 'prazo_apresentacao', None)
        representation['vigencia_inicio'] = getattr(instance, 'vigencia_inicio', None)
        representation['vigencia_fim'] = getattr(instance, 'vigencia_fim', None)

        representation['enderecos'] = EnderecoSerializer(instance.enderecos.all(), many=True).data
        representation['telefones'] = TelefoneSerializer(instance.telefones.all(), many=True).data

        return representation
    
    
#FIM SERIALIZADORES RELATIVOS AO EVENTO INCLUIR PRESTADOR#  
    
    
    

class AtivoSerializer(serializers.Serializer):
    ativo = serializers.BooleanField(required=True)

    def validate_ativo(self, value):
        """
        Validação adicional, caso necessário.
        """
        if not isinstance(value, bool):
            raise serializers.ValidationError("O campo 'ativo' deve ser um valor booleano (true/false).")
        return value



    



class TelefoneWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = '__all__'  # Include all fields from the model

class TelefoneReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Telefone
        fields = '__all__'  # Include all fields from the model
        
class EnderecoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'  # Include all fields from the model

class EnderecoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        fields = '__all__'  # Include all fields from the model
        model = Endereco




class EntidadeSocialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadeSocial
        exclude = ("polymorphic_ctype",)

class EntidadeSocialReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = EntidadeSocial
        exclude = ("polymorphic_ctype",)




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class PrestadorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestador
        exclude = ("polymorphic_ctype",)
        

from apps.atendimento.serializers import ExecucaoReadSerializer
class PrestadorReadSerializer(serializers.ModelSerializer):
    execucoes = ExecucaoReadSerializer(many=True, read_only=True, source='prestador_execucao')
    class Meta:
        depth = 1
        model = Prestador
        exclude = ("polymorphic_ctype",)
        

class ResponsavelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        exclude = ("polymorphic_ctype",)
class ResponsavelReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Responsavel
        exclude = ("polymorphic_ctype",)

class TecnicoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        exclude = ("polymorphic_ctype",)
class TecnicoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Tecnico
        exclude = ("polymorphic_ctype",)
        
class FiscalWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiscal
        exclude = ("polymorphic_ctype",)
class FiscalReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Fiscal
        exclude = ("polymorphic_ctype",)

class CoordenadorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador
        exclude = ("polymorphic_ctype",)
class CoordenadorReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Coordenador
        exclude = ("polymorphic_ctype",)

        

#==========SERIALIZADORES DE CADASTROS===========#
class CadastroTecnicoWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Tecnico
        fields = ['identificacao', 'email_contato', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        
        nome = validated_data.get('first_name', '') + " " + validated_data.get('last_name', '')
        validated_data['nome'] = nome.strip()  # Atribui o nome concatenado ao campo 'nome'
        
        validated_data.pop('password')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        return super().create(validated_data)



class CadastroFiscalWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Fiscal
        fields = ['identificacao', 'email_contato', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        
        nome = validated_data.get('first_name', '') + " " + validated_data.get('last_name', '')
        validated_data['nome'] = nome.strip()  # Atribui o nome concatenado ao campo 'nome'
        
        validated_data.pop('password')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        return super().create(validated_data)


class CadastroCoordenadorWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Coordenador
        fields = ['identificacao', 'email_contato', 'password', 'first_name', 'last_name']  # Inclua os campos relevantes do Coordenador

    def create(self, validated_data):
        """
        Remove o campo de senha antes de salvar o Coordenador,
        pois o User será criado em perform_create.
        """
        
        nome = validated_data.get('first_name', '') + " " + validated_data.get('last_name', '')
        validated_data['nome'] = nome.strip()  # Atribui o nome concatenado ao campo 'nome'
        
        validated_data.pop('password')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        return super().create(validated_data)


class CadastroResponsavelWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Responsavel
        fields = [ 'identificacao', 'email_contato', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        
        nome = validated_data.get('first_name', '') + " " + validated_data.get('last_name', '')
        validated_data['nome'] = nome.strip()  # Atribui o nome concatenado ao campo 'nome'
        
        validated_data.pop('password')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        return super().create(validated_data)



#==========FIM SERIALIZADORES DE CADASTROS===========#



#==========SERIALIZADORES DE ATIVAR E DESATIVAR ENTIDADE=========#
class EntidadeSocialAtivarDesativarSerializer(serializers.ModelSerializer):
    ativo= serializers.BooleanField(required=True)
    class Meta:
        model = EntidadeSocial
        fields = ['ativo']

    def update(self, instance, validated_data):
        instance.ativo = validated_data.get('ativo', instance.ativo)
        instance.save()
        return instance
#=================================================================#





#===================AREA DO ADMIN SERIALIZERS==============#


from apps.alocacao.models import Presenca,Vaga
from apps.encaminhamento.models import Funcao,SetorInstitucional,UnidadeOrganizacional

class AreaAdminPresencaSerializer(serializers.ModelSerializer):
    checkin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    checkout = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True)
    class Meta:
        model = Presenca
        fields = ['id','checkin', 'checkout', 'observacao_checkin', 'observacao_checkout', 'tempo_intervalo']

class AreaAdminFuncaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcao
        fields = ['id','nome']



class AreaAdminUnidadeOrganizacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeOrganizacional
        fields = ['id','nome']

class AreaAdminResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ['id','nome']
        
    
class AreaAdminSetorInstitucionalSerializer(serializers.ModelSerializer):
    unidades_organizacionais = AreaAdminUnidadeOrganizacionalSerializer(many=True)
    responsavel = AreaAdminResponsavelSerializer()
    
    class Meta:
        model = SetorInstitucional
        fields = ['id','nome','unidades_organizacionais','responsavel']

class AreaAdminVagaSerializer(serializers.ModelSerializer):
    funcao = AreaAdminFuncaoSerializer()
    setores_institucionais = AreaAdminSetorInstitucionalSerializer(many=True)

    class Meta:
        model = Vaga
        fields = ['id','funcao', 'setores_institucionais']

class AreaAdminTecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tecnico
        fields=['id','nome','identificacao']
        
class AreaAdminAlocacaoSerializer(serializers.ModelSerializer):
    vaga = AreaAdminVagaSerializer()
    presencas = AreaAdminPresencaSerializer(many=True)
    tecnico= AreaAdminTecnicoSerializer()

    class Meta:
        model = Alocacao
        fields = ['id','tecnico','prazo_apresentacao', 'data_apresentacao', 'vigencia_inicio', 'vigencia_fim', 'status', 'vaga', 'presencas']

class AreaAdminHistoricoCargaHorariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoCargaHoraria
        fields = ['id','carga_horaria_total', 'data_inicio']


        
class PrestadorSerializer(serializers.ModelSerializer):
    telefones=TelefoneSerializer(many=True)
    enderecos = EnderecoSerializer(many=True)
    class Meta:
        model = Prestador 
        fields = '__all__'  
        
class AreaAdminExecucaoSerializer(serializers.ModelSerializer):
    prestador = PrestadorSerializer()

    class Meta:
        model = Execucao
        fields = ['id','num_processo', 'rji', 'status', 'prestador']



#=============FIM AREA DO ADMIN SERIALIZERS=================#