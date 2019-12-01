from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='usuarios/media', null=True)
    tipo = models.CharField(max_length=10, null=True)
