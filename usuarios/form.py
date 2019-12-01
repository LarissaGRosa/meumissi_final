from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from usuarios.models import Perfil


class UserModelForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Primeiro Nome', required=False, help_text='Não obrigatório')
    last_name = forms.CharField(max_length=30, label='Sobrenome', required=False, help_text='Não obrigatório')
    email = forms.EmailField(max_length=254, help_text='Você precisa informar um e-mail válido')
    username = forms.CharField(max_length=30, label='Nome de usuário', required=True,
                               help_text='Obrigatório. 150 caracteres ou menos. Apenas letras, digitos e @/./+/-/')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'password1': 'Senha',
            'password2': 'Repita a senha',
        }
        help_texts = {
            'password1': 'A senha não pode ser muito similar à suas outras informações pessoais, deve ter ao menos '
                         '8 caracteres contendo letras e números e não pode ser muito comum.',
            'password2': 'Para verificar, digite a mesma senha de cima.',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 12}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'maxlenght': 12}),
        }

        def save(self, commit=True):
            user = super(UserModelForm, self).save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user


class PerfilForm(ModelForm):
    foto = forms.ImageField()

    class Meta:
        model = Perfil
        fields = ['foto']

        def save(self, commit=True):
            perfil = super(PerfilForm, self).save(commit=False)
            if commit:
                perfil.save()
            return perfil
