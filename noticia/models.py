from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    data_publi = models.DateTimeField()
    resumo = models.TextField(max_length=200)
    autor = models.CharField(max_length=30)
    foto = models.ImageField(upload_to='noticias', blank=True)

    def __str__(self):
        return "%s noticia: %s" % (self.titulo, self.descricao)

