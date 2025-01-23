from django.contrib import admin
from .models import Instituicao, UnidadeOrganizacional, SetorInstitucional, Vaga, Funcao



# Inline para Unidades Organizacionais em Instituição
class UnidadeOrganizacionalInline(admin.TabularInline):
    model = Instituicao.unidades_organizacionais.through
    extra = 0
    verbose_name = "Unidade Organizacional"
    verbose_name_plural = "Unidades Organizacionais"

class SetorInstitucionalInline(admin.TabularInline):
    model = UnidadeOrganizacional.setores_institucionais.through
    extra = 0
    verbose_name = "Setor Institucional"
    verbose_name_plural = "Setores Institucionais"



@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']
    list_per_page = 25
    ordering = ['-id']
    inlines = [UnidadeOrganizacionalInline]  # Adiciona o inline das Unidades Organizacionais

    # Remove o campo 'unidades_organizacionais' do formulário padrão
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'unidades_organizacionais' in form.base_fields:
            del form.base_fields['unidades_organizacionais']
        return form


@admin.register(UnidadeOrganizacional)
class UnidadeOrganizacionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'hora_abertura', 'hora_fechamento', 'latitude', 'longitude']
    list_display_links = ['id', 'hora_abertura', 'hora_fechamento', 'latitude', 'longitude']
    search_fields = ['id', 'hora_abertura', 'hora_fechamento', 'latitude', 'longitude']
    list_per_page = 25
    ordering = ['-id']
    
    inlines = [SetorInstitucionalInline]  # Adiciona o inline das Unidades Organizacionais

    # Remove o campo '' do formulário padrão
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'setores_institucionais' in form.base_fields:
            del form.base_fields['setores_institucionais']
        return form


@admin.register(SetorInstitucional)
class SetorInstitucionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ['id', 'nome']
    search_fields = ['id', 'nome']
    list_per_page = 25
    ordering = ['-id']


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    list_display_links = ['id', 'nome']
    search_fields = ['id', 'nome']
    list_per_page = 25
    ordering = ['-id']
    

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']
    list_per_page = 25
    ordering = ['-id']



