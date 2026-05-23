from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Servico, Agendamento, Perfil
from .forms import CadastroClienteForm


def index(request):
    return render(request, 'Agendamentos/index.html')


def redirecionar_pos_login(request):
    # Roteamento pós-login: Staff vai para o Admin, cliente para a vitrine
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    return redirect('index')


@login_required
def fazer_agendamento(request, agendamento_id=None):
    agendamento = None
    servicos_do_agendamento_ids = []

    if agendamento_id:
        agendamento = get_object_or_404(Agendamento, id=agendamento_id, cliente=request.user)
        if not agendamento.pode_alterar_online():
            messages.error(request, "Este agendamento não pode mais ser alterado online.")
            return redirect('historico_agendamentos')
        servicos_do_agendamento_ids = list(agendamento.servicos.values_list('id', flat=True))

    if request.method == 'POST':
        data_hora_str = request.POST.get('data_horario')
        servicos_selecionados = request.POST.getlist('servicos')
        observacoes = request.POST.get('observacoes', '')
        ignorar_aviso = request.POST.get('ignorar_aviso') == 'true'

        if not servicos_selecionados or not data_hora_str:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            servicos = Servico.objects.all()
            return render(request, 'Agendamentos/criar_agendamento.html', {'servicos': servicos, 'agendamento': agendamento, 'servicos_do_agendamento_ids': servicos_do_agendamento_ids})

        data_hora_obj = parse_datetime(data_hora_str)
        if not data_hora_obj:
            messages.error(request, "Formato de data inválido.")
            servicos = Servico.objects.all()
            return render(request, 'Agendamentos/criar_agendamento.html', {'servicos': servicos, 'agendamento': agendamento, 'servicos_do_agendamento_ids': servicos_do_agendamento_ids})

        data_hora_obj = timezone.make_aware(data_hora_obj)

        if data_hora_obj < timezone.now():
            messages.error(request, "Você não pode agendar um horário no passado!")
            servicos = Servico.objects.all()
            return render(request, 'Agendamentos/criar_agendamento.html', {'servicos': servicos, 'agendamento': agendamento, 'servicos_do_agendamento_ids': servicos_do_agendamento_ids})

        # Regra de Negócio: Impede múltiplos agendamentos ativos na mesma semana
        inicio_semana = data_hora_obj.date() - timedelta(days=data_hora_obj.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        query_semana = Agendamento.objects.filter(
            cliente=request.user,
            data_hora__date__range=[inicio_semana, fim_semana]
        ).exclude(status='CANCELADO')
        
        if agendamento:
            query_semana = query_semana.exclude(id=agendamento.id)

        existente = query_semana.first()

        if existente and not ignorar_aviso:
            if existente.pode_alterar_online():
                # Retorna dados de contexto para acionar o modal de confirmação no front-end
                servicos = Servico.objects.all()
                return render(request, 'Agendamentos/criar_agendamento.html', {
                    'servicos': servicos,
                    'agendamento': agendamento,
                    'servicos_do_agendamento_ids': servicos_do_agendamento_ids,
                    'conflito_semana': existente,
                    'dados_post': request.POST
                })
            else:
                # Bloqueia se violar a antecedência mínima da regra de 2 dias
                messages.error(request, f"Você já possui o agendamento ({existente.data_hora.strftime('%d/%m/%Y')}) nessa semana. Como falta menos de 2 dias para ele, não é possível alterá-lo online. Agende para próxima semana ou entre em contato.")
                servicos = Servico.objects.all()
                return render(request, 'Agendamentos/criar_agendamento.html', {'servicos': servicos, 'agendamento': agendamento, 'servicos_do_agendamento_ids': servicos_do_agendamento_ids})

        # Persistência ou atualização do agendamento
        if agendamento:
            agendamento.data_hora = data_hora_obj
            agendamento.status = 'PENDENTE'
            agendamento.save()
            messages.success(request, "Agendamento atualizado com sucesso!")
        else:
            agendamento = Agendamento.objects.create(
                cliente=request.user,
                data_hora=data_hora_obj
            )
            messages.success(request, "Agendamento solicitado com sucesso!")
        
        agendamento.servicos.set(servicos_selecionados)
        return redirect('historico_agendamentos')

    return render(request, 'Agendamentos/criar_agendamento.html', {
        'servicos': Servico.objects.all(), 
        'agendamento': agendamento,
        'servicos_do_agendamento_ids': servicos_do_agendamento_ids
    })


@login_required
def historico_agendamentos(request):
    base_query = Agendamento.objects.filter(cliente=request.user)
    
    # Listagens segregadas por status e ordenação cronológica/reversa
    agendamentos_ativos = base_query.filter(status__in=['PENDENTE', 'CONFIRMADO']).order_by('data_hora')
    agendamentos_finalizados = base_query.filter(status__in=['CONCLUIDO', 'CANCELADO']).order_by('-data_hora')

    return render(request, 'Agendamentos/historico.html', {
        'agendamentos_ativos': agendamentos_ativos,
        'agendamentos_finalizados': agendamentos_finalizados,
    })


def cadastrar_cliente(request):
    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            email_limpo = form.cleaned_data['email'].lower().strip()
            username_interno = email_limpo.replace('@', '').replace('.', '')

            user = User.objects.create_user(
                username=username_interno,
                email=email_limpo,
                password=form.cleaned_data['password']
            )
            
            Perfil.objects.create(
                usuario=user,
                nome=form.cleaned_data['nome'],
                email=email_limpo,
                celular=form.cleaned_data['celular'],
                cep=form.cleaned_data['cep'],
                rua=form.cleaned_data['rua'],
                numero=form.cleaned_data['numero'],
                cidade=form.cleaned_data['cidade'],
                estado=form.cleaned_data['estado']
            )
            messages.success(request, "Conta criada com sucesso! Já pode fazer o seu login.")
            return redirect('login')
    else:
        form = CadastroClienteForm()
        
    return render(request, 'Agendamentos/cadastro.html', {'form': form})


def login_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('password', '')

        if not email or not senha:
            messages.error(request, "Por favor, preencha o e-mail e a senha.")
            return render(request, 'Agendamentos/login.html')

        try:
            # Autenticação baseada em e-mail através do mapeamento do username interno
            usuario = User.objects.get(email=email)
            user = authenticate(request, username=usuario.username, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', '/agendar/'))
            else:
                messages.error(request, "Senha incorreta. Tente novamente.")
        except User.DoesNotExist:
            messages.error(request, "E-mail não cadastrado em nosso sistema.")

    return render(request, 'Agendamentos/login.html')


@login_required
def cancelar_agendamento(request, agendamento_id):
    if request.method == 'POST':
        agendamento = get_object_or_404(Agendamento, id=agendamento_id, cliente=request.user)
        agendamento.status = 'CANCELADO'
        agendamento.save()
        messages.success(request, "Agendamento cancelado com sucesso!")
    
    return redirect('historico_agendamentos')