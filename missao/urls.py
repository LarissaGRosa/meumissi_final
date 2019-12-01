from django.urls import path

from . import views

app_name = 'missao'

urlpatterns = [
    path('', views.list_missao, name='listamissao'),
    path('<int:pk>/entrar', views.user_missao, name='entrar'),
]