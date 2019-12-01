from django.db import models
from django.conf import settings


class Missoes(models.Model):
    mestre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500)
    utilidade = models.TextField(max_length=400)
    pontos = models.IntegerField()
    isValid = models.BooleanField(default=False)
    arquivo = models.FileField(upload_to='documents/', blank=True)
    patrocinador = models.TextField(blank=True, null=True)
    premio = models.CharField(max_length=300, blank=True)
    cod_premio = models.CharField(max_length=30, blank=True)
    isTrocado = models.BooleanField(default=False)
    isTerminada = models.BooleanField(default=False)

    def criar(self):
        self.save()

    def validar(self):
        self.isValid = True
        self.save()

    def __str__(self):
        return "%s missao: %s" % (self.titulo, self.descricao)


class Usuariomissao(models.Model):
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_missao = models.ForeignKey(Missoes, on_delete=models.CASCADE)
    is_desistido = models.BooleanField(default=False)
    is_concluido = models.BooleanField(default=False)
    is_ganhador = models.BooleanField(default=False)

