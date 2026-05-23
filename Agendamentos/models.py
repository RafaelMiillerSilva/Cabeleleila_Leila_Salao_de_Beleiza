from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    duracao_minutos = models.IntegerField(default=30)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CONCLUIDO', 'Concluido'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    servicos = models.ManyToManyField(Servico, related_name='agendamentos')
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    @property
    def preco_total(self):
        return sum(servico.preco for servico in self.servicos.all())

    def pode_alterar_online(self):
        # Valida antecedência mínima de 48h e impede alteração de horários passados
        agora = timezone.now()
        if self.data_hora < agora or (self.data_hora - agora) < timedelta(days=2):
            return False
        return True

    def buscar_agendamento_na_mesma_semana(self):
        # Retorna agendamento ativo do cliente na mesma semana (segunda a domingo)
        data_apenas = self.data_hora.date()
        inicio_semana = data_apenas - timedelta(days=data_apenas.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        
        return Agendamento.objects.filter(
            cliente=self.cliente,
            data_hora__date__range=[inicio_semana, fim_semana]
        ).exclude(id=self.id).first()


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=20)
    
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return self.nome