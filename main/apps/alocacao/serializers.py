from rest_framework import serializers
from .models import (
    Alocacao,DiaCombinado,Presenca
)
from apps.socialentity.models import Prestador
from apps.atendimento.models import Execucao,Condicao

class AlocacaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        exclude = ("polymorphic_ctype",)

class AlocacaoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Alocacao
        exclude = ("polymorphic_ctype",)


#===Serializadores de Busca de Alocacao By Setor===#

class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = ['id']

#==================================================#



class PresencaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        exclude = ("polymorphic_ctype",)


class PresencaReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Presenca
        exclude = ("polymorphic_ctype",)


class DiaCombinadoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaCombinado
        exclude = ("polymorphic_ctype",)


class DiaCombinadoReadSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = DiaCombinado
        exclude = ("polymorphic_ctype",)





#=============SERIALIZERS CHECKIN CHECKOUT===============#

class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = ['id', 'checkin', 'observacao_checkin']
        read_only_fields = ['id']

from datetime import timedelta
class TimedeltaField(serializers.Field):
    """
    Custom field to handle timedelta objects. It serializes timedelta as HH:MM:SS and deserializes from HH:MM:SS format.
    """
    def to_representation(self, value):
        # Convert timedelta to HH:MM:SS string
        if isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return None

    def to_internal_value(self, data):
        # Convert HH:MM:SS string to timedelta
        try:
            hours, minutes, seconds = map(int, data.split(":"))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            raise serializers.ValidationError("Invalid time format, expected HH:MM:SS.")

class TimedeltaField(serializers.Field):
    def to_representation(self, value):
        return str(value)  # Retorna o timedelta como string

    def to_internal_value(self, data):
        try:
            hours, minutes, seconds = map(int, data.split(':'))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            raise serializers.ValidationError("O valor deve estar no formato HH:MM:SS.")

class CheckoutSerializer(serializers.ModelSerializer):
    
    tempo_intervalo = TimedeltaField(required=False)  # Campo personalizado

    class Meta:
        model = Presenca
        fields = ['id', 'checkin', 'checkout', 'observacao_checkout', 'tempo_intervalo']
        read_only_fields = ['id', 'checkin', 'checkout']

    def to_representation(self, instance):
        from datetime import datetime, timedelta
        """
        Força a formatação uniforme para todos os campos de data e hora.
        """
        data = super().to_representation(instance)

        # Verifica e formata o campo checkin
        if instance.checkin:
            if isinstance(instance.checkin, str):
                try:
                    instance.checkin = datetime.fromisoformat(instance.checkin)
                except ValueError:
                    raise serializers.ValidationError("Formato inválido para o campo 'checkin'.")
            data['checkin'] = instance.checkin.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Verifica e formata o campo checkout
        if instance.checkout:
            if isinstance(instance.checkout, str):
                try:
                    instance.checkout = datetime.fromisoformat(instance.checkout)
                except ValueError:
                    raise serializers.ValidationError("Formato inválido para o campo 'checkout'.")
            data['checkout'] = instance.checkout.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        return data
        
class CheckoutComHoraSerializer(serializers.ModelSerializer):
    tempo_intervalo = TimedeltaField(required=False)  # Use the custom TimedeltaField

    class Meta:
        model = Presenca
        fields = ['id', 'checkin', 'checkout', 'observacao_checkout', 'tempo_intervalo']
        read_only_fields = ['id', 'checkin']
        
#===========FIM SERIALIZERS CHECKIN CHECKOUT===============#



#========================#
from apps.socialentity.models import Prestador
class PrestadorSerializer(serializers.ModelSerializer):
    prestador_id = serializers.IntegerField()
    alocacao_id = serializers.IntegerField()
    execucao_id = serializers.IntegerField()
    condicao_id = serializers.IntegerField()
    nome_social = serializers.CharField()
    foto = serializers.ImageField()
    rg = serializers.CharField()
    escolaridade = serializers.CharField()
    situacao_economica = serializers.CharField()
    
#===========fim =============#