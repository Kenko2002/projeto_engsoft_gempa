from django.contrib import admin
from .models import Endereco,Telefone,EntidadeSocial,Usuario,Prestador,Tecnico,Fiscal,Coordenador,Responsavel
from apps.atendimento.models import Execucao,Condicao,HistoricoCargaHoraria
'''
@admin.register(EntidadeSocial)
class EntidadeSocialAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'identificacao', 'ativo', 'email_contato']
    list_display_links = ['id', 'nome', 'identificacao', 'ativo', 'email_contato']
    search_fields = ['id', 'nome', 'identificacao', 'ativo', 'email_contato']
    list_per_page = 25
    ordering = ['-id']
'''
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']
    list_per_page = 25
    ordering = ['-id']
    
    





class ExecucaoInline(admin.TabularInline):
    model = Execucao
    fields = ('num_processo','rji','status','condicoes','observacoes')  # Ajuste os campos conforme necessário
    extra = 0  # Quantidade de instâncias vazias para criação de novas Execuções




# Agora defina o Admin para o Prestador
@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'foto', 'rg', 'nome_social', 'escolaridade', 'situacao_economica', 'descricao_avaliacao_psicosocial']
    list_display_links = ['id', 'foto', 'rg', 'nome_social', 'escolaridade', 'situacao_economica', 'descricao_avaliacao_psicosocial']
    search_fields = ['id', 'foto', 'rg', 'nome_social', 'escolaridade', 'situacao_economica', 'descricao_avaliacao_psicosocial']
    list_per_page = 25
    ordering = ['-id']
    
    # Adiciona o formulário de Execucao no formulário de Prestador
    inlines = [ExecucaoInline]

    def save_model(self, request, obj, form, change):
        """Atualiza ou cria uma Execução ao salvar um Prestador."""
        super().save_model(request, obj, form, change)

        # Obtém o número de processo informado no formulário
        num_processo = form.cleaned_data.get('num_processo')
        if num_processo:
            # Verifica se já existe uma execução associada ao Prestador
            execucao, created = Execucao.objects.get_or_create(prestador=obj)
            execucao.num_processo = num_processo
            execucao.save()
            
            
            
            

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['id',]
    list_display_links = ['id',]
    search_fields = ['id',]
    list_per_page = 25
    ordering = ['-id']

@admin.register(Fiscal)
class FiscalAdmin(admin.ModelAdmin):
    list_display = ['id',]
    list_display_links = ['id',]
    search_fields = ['id',]
    list_per_page = 25
    ordering = ['-id']

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ['id',]
    list_display_links = ['id',]
    search_fields = ['id',]
    list_per_page = 25
    ordering = ['-id']

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ['id',]
    list_display_links = ['id',]
    search_fields = ['id',]
    list_per_page = 25
    ordering = ['-id']




@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'cep']
    list_display_links = ['id', 'logradouro']
    search_fields = ['logradouro', 'bairro', 'cidade', 'estado', 'cep']
    list_per_page = 25
    ordering = ['id']


@admin.register(Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero', 'ddd']
    list_display_links = ['id', 'numero']
    search_fields = ['numero', 'ddd']
    list_per_page = 25
    ordering = ['id']
