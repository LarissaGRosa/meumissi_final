from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from typing import Set
from django.contrib import admin
from missao.models import Missoes
from usuarios.models import Perfil

admin.site.register(Perfil)




