from django.contrib.auth.models import User
from django.shortcuts import render

from missao.form import Usermissaoform
from missao.models import Missoes, Usuariomissao


def list_missao(request):
    missoes = Missoes.objects.exclude(patrocinador=None).filter(isTerminada=False)
    return render(request, 'missao/missoes.html', {'missoes': missoes})


def user_missao(request, pk):
    missoes = Missoes.objects.filter(isValid=True)
    user = User.objects.get(id=request.user.id)
    missao = Missoes.objects.get(id=pk)
    mymodel = Usuariomissao.objects.filter(id_missao=missao, id_usuario=user).count()
    if mymodel > 0:
        return render(request, 'missao/naoentrei.html', {'missoes': missoes})
    elif missao.mestre == user:
        return render(request, 'missao/naoentrei.html', {'missoes': missoes})

    else:
        usuariomissao = Usuariomissao(id_usuario=user, id_missao=missao, is_desistido=False, is_concluido=False,
                                      is_ganhador=False)
        usuariomissao.save()
        return render(request, 'missao/entrei.html', {'missoes': missoes})
