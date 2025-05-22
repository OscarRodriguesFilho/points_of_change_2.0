from django.contrib import admin

# Register your models here.
from .models import Tarefa, Recomendacao


admin.site.register(Tarefa)
admin.site.register(Recomendacao)