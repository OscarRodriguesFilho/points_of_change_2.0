from django.db import models

# Create your models here.

from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    recomendacao = models.ForeignKey('Recomendacao', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('usuario', 'recomendacao')  # impede múltiplos likes do mesmo user



class Recomendacao(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)

    nome_postador = models.CharField(max_length=100)
    cargo_postador = models.CharField(max_length=100)

    arquivo = models.FileField(upload_to='recomendacoes_pdfs/')

    def __str__(self):
        return self.titulo




class Tarefa(models.Model):
    """
    Model para armazenar tarefas com pontuação, usuário, tipo e estado de conclusão.

    Campos:
    - id: PK automática                                           ok
    - tarefa: descrição da tarefa                                 ok
    - pontos: valor numérico da tarefa                            ok
    - usuario: FK para o usuário que criou a tarefa               ok
    - tipo: categoria (diária, semanal, aleatória)                ok
    - estado: indica se foi concluída (True) ou não (False)       ok
    - created_at: timestamp de criação                            ok
    """
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,  default=1)
    tarefa = models.TextField(verbose_name='Descrição da tarefa')
    pontos = models.PositiveIntegerField(verbose_name='Pontuação')
    estado = models.BooleanField(
        default=False,
        verbose_name='Estado'
    )
    tipo = models.CharField(max_length=20, default="Avulso")
    data = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        status = '✔' if self.estado else '✖'
        return f"{status} {self.tarefa[:50]} ({self.pontos} pts)"

class Novo_tipo(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,  default=1)
    nome = models.TextField(verbose_name='Descrição da lista', default="Avulso")
    meta = models.PositiveIntegerField(verbose_name='Meta', default="0")