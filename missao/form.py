from django.forms import ModelForm
from django import forms
from .models import Missoes, Usuariomissao
from django.contrib.auth.models import User


class Addmissao(ModelForm):
    arquivo = forms.FileField()
    titulo = forms.CharField(max_length=30, label='Título', required=True)
    descricao = forms.CharField(max_length=500, label='Descrição', required=True)
    utilidade = forms.CharField(max_length=300, label='Utilidade', required=True)

    class Meta:
        model = Missoes
        fields = ('titulo', 'descricao', 'utilidade', 'arquivo')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 1000}),
            'utilidade': forms.TextInput(attrs={'class': 'form-control', 'maxlenght': 255}),
        }

        def save(self, commit=True):
            missao = super(Addmissao, self).save(commit=False)
            if commit:
                missao.save()
            return missao


class Usermissaoform(ModelForm):

    class Meta:
        model = Usuariomissao
        fields = ('id_usuario', 'id_missao')


class Patrocinamissao(ModelForm):
    premio = forms.CharField(max_length=30, label='Prêmio', required=True)
    cod_premio = forms.CharField(max_length=30, label='Código para resgate', required=True)

    class Meta:
        model = Missoes
        fields = ('premio', 'cod_premio')


