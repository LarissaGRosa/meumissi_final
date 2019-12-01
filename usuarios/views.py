from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from missao.form import Addmissao, Patrocinamissao
from missao.models import Missoes, Usuariomissao
from usuarios.form import UserModelForm, PerfilForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from usuarios.models import Perfil


def cadastro(request):
    form = UserModelForm(request.POST or None)
    msg = 'Não pode haver dois usuários com o mesmo e-mail'
    context = {'form': form, 'msg': msg}
    if request.method == 'POST':
        if form.is_valid():
            try:
                usuario_aux = User.objects.get(email=request.POST['email'])
                if usuario_aux:
                    msg = 'Erro! Já existe um usuário com o mesmo e-mail'
                    return render(request, 'usuarios/cadastro.html', {'msg': msg, 'form': form})

            except User.DoesNotExist:
                form.save()
                msg = 'Usuário cadastrado com sucesso'
                return render(request, 'usuarios/cadastro.html', {'msg': msg, 'form': form})
    return render(request, 'usuarios/cadastro.html', context)


def do_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('noticias:post_list')
    return render(request, 'usuarios/login.html')


def do_logout(request):
    logout(request)
    return redirect('noticias:post_list')


@login_required()
def perfil(request):
    if request.method == "POST":
        perfil_user, created = Perfil.objects.get_or_create(user=request.user)
        form1 = PerfilForm(request.POST or None, request.FILES or None, instance=perfil_user)
        form = Addmissao(request.POST or None, request.FILES or None)
        user = User.objects.get(id=request.user.id)
        user_name = request.user.first_name
        user_email = request.user.email
        missoes = Missoes.objects.filter(mestre=user)
        if form1.is_valid():
            perfil_user = form1
            perfil_user.user = user
            perfil_user.save()
            return render(request, 'usuarios/cadastrosucess.html',
                          )

    else:
        form = Addmissao()
        form1 = PerfilForm()
        user = User.objects.get(id=request.user.id)
        missoes = Missoes.objects.filter(mestre=user)
        user_name = request.user.first_name
        user_email = request.user.email
        perfil_user = Perfil.objects.filter(user=user)
        if perfil_user:
            perfil_user = Perfil.objects.get(user=user)
            return render(request, 'usuarios/perfil.html',
                          {'user_email': user_email, 'user_name': user_name, 'form': form, 'missoes': missoes,
                           'form1': form1, 'perfil': perfil_user})
        else:
            return render(request, 'usuarios/perfil.html',
                          {'user_email': user_email, 'user_name': user_name, 'form': form, 'missoes': missoes,
                           'form1': form1})


def criarmissi(request):
    if request.method == "POST":

        form = Addmissao(request.POST or None, request.FILES or None)
        user = User.objects.get(id=request.user.id)

        if form.is_valid():
            missao = form.save(commit=False)
            missao.mestre = user
            missao.isValid = False
            missao.pontos = 1
            missao.isTrocado = False
            missao.isTerminado = False
            missao.premio = 'nada ainda'
            missao.cod_premio = 'nada ainda'
            missao.save()
            return render(request, 'usuarios/cadastrosucess.html')


def finalizar1(request, pk):
    missao = Missoes.objects.get(id=pk)
    participantes = Usuariomissao.objects.select_related('id_usuario').filter(id_missao=missao)
    return render(request, 'usuarios/finalizar.html', {'participantes': participantes, 'missao': missao})


@login_required
def finalizar2(request, pk):
    if request.method == 'POST':
        ganhador = request.POST.get('Ganhador')
        user = User.objects.get(id=ganhador)
        missao = Missoes.objects.get(id=pk)
        um = Usuariomissao.objects.get(id_missao=missao, id_usuario=user)
        missao.isTerminada = True
        missao.save()
        um.is_ganhador = True
        um.save()
        return render(request, 'noticia/index.html')


def missi(request):
    user = User.objects.get(id=request.user.id)
    mymissoes = Usuariomissao.objects.select_related('id_missao').filter(id_usuario=user)
    return render(request, 'usuarios/minhasmissoes.html', {'mymissoes': mymissoes})


def desistir(request, pk):
    user = User.objects.get(id=request.user.id)
    missao = Missoes.objects.get(id=pk)
    um = Usuariomissao.objects.get(id_missao=missao, id_usuario=user)
    um.is_desistido = True
    um.save()
    mymissoes = Usuariomissao.objects.select_related('id_missao').filter(id_usuario=user)
    return render(request, 'usuarios/minhasmissoes.html', {'mymissoes': mymissoes})


def status(request):
    user = User.objects.get(id=request.user.id)
    mymissoes = Usuariomissao.objects.select_related('id_missao').filter(id_usuario=user)
    return render(request, 'usuarios/finalizadas.html', {'mymissoes': mymissoes})


def patrocine(request):
    missoes = Missoes.objects.filter(patrocinador='')
    user = User.objects.get(id=request.user.id)
    perfil2 = Perfil.objects.get(user=user)
    missao = Missoes.objects.filter(patrocinador=perfil2.tipo)
    patrocina = Patrocinamissao()
    return render(request, 'usuarios/patrocine.html', {'missoes': missoes, 'form': patrocina, 'quantia': missao})


def escolhapatrocinio(request):
    if request.method == "POST":
        form = Patrocinamissao(request.POST or None)
        if form.is_valid:
            missao = request.POST.get('patrocinar')
            missao1 = Missoes.objects.get(id=missao)
            user = User.objects.get(id=request.user.id)
            perfil1 = Perfil.objects.get(user=user)
            missao1.patrocinador = perfil1.tipo
            missao1.cod_premio = request.POST.get('cod_premio')
            missao1.premio = request.POST.get('premio')
            missao1.save()
            return render(request, 'usuarios/confirmar1.html')


def trocarpremio(request):
    user = User.objects.get(id=request.user.id)
    perfil2 = Perfil.objects.get(user=user)
    missao= Missoes.objects.filter(patrocinador=perfil2.tipo, isTrocado=False)
    return render(request, 'usuarios/trocarpremio.html', {'missoes': missao})


def trocarpremio2(request, pk):
    missao = Missoes.objects.get(id=pk)
    missao.isTrocado = True
    missao.save()
    return render(request, 'usuarios/confirmar2.html')








