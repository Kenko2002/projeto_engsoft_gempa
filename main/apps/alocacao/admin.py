from django.contrib import admin
from .models import Alocacao,Presenca,DiaCombinado
    
class PresencaInline(admin.TabularInline):
    model = Alocacao.presencas.through
    extra = 0
    verbose_name = "Presenca"
    verbose_name_plural = "Presencas"
    ordering = ['-presenca__checkin']  

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-presenca__checkin')
    
    
    
    
    
class DiasCombinadosInline(admin.TabularInline):
    model = Alocacao.diascombinados.through
    extra = 0
    verbose_name = "DiasCombinados"
    verbose_name_plural = "DiasCombinados"
    
    
    
    
@admin.register(Alocacao)
class AlocacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'observacao_avaliacao','prazo_apresentacao', 'data_apresentacao', 'vigencia_inicio', 'vigencia_fim']
    list_display_links = ['id', 'observacao_avaliacao','prazo_apresentacao', 'data_apresentacao', 'vigencia_inicio', 'vigencia_fim']
    search_fields = ['id', 'observacao_avaliacao','prazo_apresentacao', 'data_apresentacao', 'vigencia_inicio', 'vigencia_fim']
    list_per_page = 25
    ordering = ['-id']
    inlines=[PresencaInline,DiasCombinadosInline]
    exclude = ['presencas','diascombinados']
    
    
    


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ['id', 'checkin','checkout','observacao_checkin','observacao_checkout','tempo_intervalo']
    list_display_links = ['id', 'checkin','checkout','observacao_checkin','observacao_checkout','tempo_intervalo']
    search_fields = ['id','hora_cadastro_checkout','hora_cadastro_checkin', 'checkin','checkout','observacao_checkin','observacao_checkout','tempo_intervalo']
    list_per_page = 25
    ordering = ['-id']
    

@admin.register(DiaCombinado)
class DiaCombinadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'dia_semana', 'horario_entrada', 'horario_saida']
    list_display_links = ['id', 'dia_semana', 'horario_entrada', 'horario_saida']
    search_fields = ['id', 'dia_semana', 'horario_entrada', 'horario_saida']
    list_per_page = 25
    ordering = ['-id']
    
    
    
    
    
