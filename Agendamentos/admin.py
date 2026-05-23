from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Servico, Agendamento

# Configurações Globais do Painel
admin.site.site_header = "Painel Administrativo & Gerencial - Cabeleleila Leila"
admin.site.site_title = "Cabeleleila Leila"
admin.site.index_title = "Operações e Indicadores do Salão"
admin.site.site_url = '/agendar/'


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao_minutos')
    search_fields = ('nome',)
    list_editable = ('preco', 'duracao_minutos')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'lista_servicos', 'data_hora', 'status', 'exibir_valor_total')
    list_filter = ('status', 'data_hora')
    list_editable = ('status',)
    search_fields = ('cliente__username', 'cliente__first_name', 'cliente__email')
    filter_horizontal = ('servicos', )
    actions = ['confirmar_agendamentos_em_massa']

    def lista_servicos(self, obj):
        return ", ".join([s.nome for s in obj.servicos.all()])
    lista_servicos.short_description = 'Serviços Solicitados'

    def exibir_valor_total(self, obj):
        return f"R$ {obj.preco_total}"
    exibir_valor_total.short_description = 'Faturamento Previsto'

    @admin.action(description="Marcar selecionados como CONFIRMADO")
    def confirmar_agendamentos_em_massa(self, request, queryset):
        linhas_atualizadas = queryset.update(status='CONFIRMADO')
        self.message_user(request, f"{linhas_atualizadas} agendamentos foram confirmados com sucesso!")

    def changelist_view(self, request, extra_context=None):
        # Definição do intervalo cronológico da semana corrente (segunda a domingo)
        hoje = timezone.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        agendamentos_da_semana = Agendamento.objects.filter(
            data_hora__date__range=[inicio_semana, fim_semana]
        ).exclude(status='CANCELADO')

        # Injeção das métricas gerenciais no contexto do dashboard superior
        extra_context = extra_context or {}
        extra_context['gerencial'] = {
            'total_atendimentos': agendamentos_da_semana.count(),
            'confirmados': agendamentos_da_semana.filter(status='CONFIRMADO').count(),
            'pendentes': agendamentos_da_semana.filter(status='PENDENTE').count(),
            'faturamento_total': sum(a.preco_total for a in agendamentos_da_semana),
            'periodo_semana': f"{inicio_semana.strftime('%d/%m')} a {fim_semana.strftime('%d/%m')}"
        }
        
        return super().changelist_view(request, extra_context=extra_context)