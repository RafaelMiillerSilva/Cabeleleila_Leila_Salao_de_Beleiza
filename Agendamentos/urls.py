from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastrar_cliente, name='cadastro'),
    path('agendar/', views.fazer_agendamento, name='criar_agendamento'),
    path('agendar/editar/<int:agendamento_id>/', views.fazer_agendamento, name='editar_agendamento'),
    path('historico/', views.historico_agendamentos, name='historico_agendamentos'),
    path('historico/cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('login/', views.login_cliente, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('como-ficaria-redirecionar/', views.redirecionar_pos_login, name='redirecionar_pos_login'),
]
