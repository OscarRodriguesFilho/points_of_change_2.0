from django.db import models

# Create your models here.



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