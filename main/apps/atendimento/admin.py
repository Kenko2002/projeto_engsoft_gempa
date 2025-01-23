from django.contrib import admin
from .models import Atendimento,Observacao,Execucao,Condicao,HistoricoCargaHoraria

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'horario', 'motivo', 'observacao', 'justificativa_cancelamento']
    list_display_links = ['id', 'horario', 'motivo', 'observacao', 'justificativa_cancelamento']
    search_fields = ['id', 'horario', 'motivo', 'observacao', 'justificativa_cancelamento']
    list_per_page = 25
    ordering = ['-id']

@admin.register(Observacao)
class ObservacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'texto', 'link_arquivo']
    list_display_links = ['id', 'texto', 'link_arquivo']
    search_fields = ['id', 'texto', 'link_arquivo']
    list_per_page = 25
    ordering = ['-id']

@admin.register(Execucao)
class ExecucaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'num_processo', 'rji']
    list_display_links = ['id', 'num_processo', 'rji']
    search_fields = ['id', 'num_processo', 'rji']
    list_per_page = 25
    ordering = ['-id']

@admin.register(Condicao)
class CondicaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'horas_cumpridas_totais', 'flexivel_dia', 'flexivel_horario', 'horas_minimas', 'horas_maximas', 'periodo_dias']
    list_display_links = ['id', 'horas_cumpridas_totais', 'flexivel_dia', 'flexivel_horario', 'horas_minimas', 'horas_maximas', 'periodo_dias']
    search_fields = ['id', 'horas_cumpridas_totais', 'flexivel_dia', 'flexivel_horario', 'horas_minimas', 'horas_maximas', 'periodo_dias']
    list_per_page = 25
    ordering = ['-id']

@admin.register(HistoricoCargaHoraria)
class HistoricoCargaHorariaAdmin(admin.ModelAdmin):
    list_display = ['id', 'carga_horaria_total', 'data_inicio']
    list_display_links = ['id', 'carga_horaria_total', 'data_inicio']
    search_fields = ['id', 'carga_horaria_total', 'data_inicio']
    list_per_page = 25
    ordering = ['-id']

