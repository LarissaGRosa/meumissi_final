from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .tokens import user_tokenizer
from django.conf import settings
from . import views
app_name = 'usuarios'

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('login', views.do_login, name='do_login'),
    path('logout', views.do_logout, name='do_logout'),
    path('resetar', include('django.contrib.auth.urls')),
    path('perfil', views.perfil, name='perfil'),
    path('vermissi', views.missi, name='missoesandamento'),
    path('status_missi', views.status, name='status'),
    path('<int:pk>/desistir', views.desistir, name='desistir'),
    path('<int:pk>/finalizando', views.finalizar1, name='final_um'),
    path('<int:pk>/finalizandofim', views.finalizar2, name='final_dois'),
    path('sucesso', views.criarmissi, name='criarmissi'),
    path('patrocine', views.patrocine, name='patrocine'),
    path('sucesso_patrocinio', views.escolhapatrocinio, name='escolha'),
    path('trocarpremio', views.trocarpremio, name='trocarpremio'),
    path('<int:pk>/trocarpremio', views.trocarpremio2, name='trocarfim'),
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
          template_name='usuarios/reset_password.html',
          email_template_name='usuarios/reset_password_email.html',
          success_url=settings.LOGIN_URL,
          token_generator=user_tokenizer),
          name='reset_password'
      ),
    path(
        'reset-password-confirmation/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='usuarios/reset_password_update.html',
            post_reset_login=True,
            post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
            token_generator=user_tokenizer,
            success_url=settings.LOGIN_REDIRECT_URL),
        name='password_reset_confirm'
    ),

]