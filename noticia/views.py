from django.shortcuts import render
from django.utils import timezone

from noticia.models import Noticia


def post_list(request):
    noticias = Noticia.objects.filter(data_publi__lte=timezone.now()).order_by('data_publi')
    return render(request, 'noticia/index.html', {'posts': noticias})


