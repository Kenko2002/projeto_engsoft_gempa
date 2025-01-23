from rest_framework import serializers
from .models import (
    Atendimento,
    Observacao,
    Execucao,
    Condicao,
    HistoricoCargaHoraria,
)
from apps.socialentity.models import Tecnico,Prestador

class AtendimentoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        exclude = ("polymorphic_ctype",)



from apps.socialentity.models import Endereco,Telefone,Prestador
from apps.socialentity.serializers import EnderecoSerializer,TelefoneSerializer

from django.utils.timezone import now


class PrestadorSerializer(serializers.ModelSerializer):
    enderecos = EnderecoSerializer(many=True, read_only=True)
    telefones = TelefoneSerializer(many=True, read_only=True)

    class Meta:
        model = Prestador
        fields = '__all__'
    
class AtendimentoReadSerializer(serializers.ModelSerializer):
    horario = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    prestador = PrestadorSerializer(read_only=True)  # Inclui os dados expandidos

    class Meta:
        depth = 1
        model = Atendimento
        exclude = ("polymorphic_ctype",)
    
    def to_representation(self, instance):
        # Lógica para conferir e atualizar os agendamentos vencidos
        if instance.status == "AGENDADO" and instance.horario < now():
            instance.status = "EXPIRADO"
            instance.save()  # Salva a mudança no banco de dados

        # Serializa os dados após a atualização
        return super().to_representation(instance)
        
        
        


class ObservacaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        exclude = ("polymorphic_ctype",)

class ObservacaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Observacao
        exclude = ("polymorphic_ctype",)


class ExecucaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execucao
        exclude = ("polymorphic_ctype",)

class ExecucaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Execucao
        exclude = ("polymorphic_ctype",)


class CondicaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condicao
        exclude = ("polymorphic_ctype",)

class CondicaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Condicao
        exclude = ("polymorphic_ctype",)


class HistoricoCargaHorariaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoCargaHoraria
        exclude = ("polymorphic_ctype",)

class HistoricoCargaHorariaReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = HistoricoCargaHoraria
        exclude = ("polymorphic_ctype",)




#=======================ATENDIMENTO====================#
class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = ['horario', 'motivo', 'observacao', 'tecnico', 'prestador']

    def validate_tecnico(self, value):
        try:
            Tecnico.objects.get(id=value)
        except Tecnico.DoesNotExist:
            raise serializers.ValidationError("Técnico não encontrado")
        return value

    def validate_prestador(self, value):
        try:
            Prestador.objects.get(id=value)
        except Prestador.DoesNotExist:
            raise serializers.ValidationError("Prestador não encontrado")
        return value
#=========================================================#