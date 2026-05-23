# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class CadastroClienteForm(forms.ModelForm):
    nome = forms.CharField(label="Nome Completo", max_length=150)
    email = forms.EmailField(label="E-mail")
    celular = forms.CharField(label="Celular/WhatsApp", max_length=20)
    
    cep = forms.CharField(label="CEP", max_length=9)
    rua = forms.CharField(label="Rua/Logradouro", max_length=150)
    numero = forms.CharField(label="Número", max_length=20)
    cidade = forms.CharField(label="Cidade", max_length=100)
    estado = forms.CharField(label="Estado (UF)", max_length=2)

    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']  # O username é gerado dinamicamente na view

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if User.objects.filter(email=email).exists() or Perfil.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado em nosso sistema.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        
        # Garante a obrigatoriedade de preenchimento de todos os campos
        for campo, valor in cleaned_data.items():
            if not valor or str(valor).strip() == "":
                self.add_error(campo, "Este campo é de preenchimento obrigatório.")

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não conferem.")
            
        return cleaned_data