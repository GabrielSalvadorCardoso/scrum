from django.db import models

TASKS_TYPES = [('Desenvolvimneto','Desenvolvimento'),
               ('Modelagem', 'Modelagem'),
               ('Engenharia de Requisitos', 'Engenharia de Requisitos'),
               ('Omologação', 'Omologação'),('Testes', 'Testes')]

class Tarefa(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=100, blank=False)
    tipo = models.CharField(choices=TASKS_TYPES, max_length=100)

    class Meta:
        ordering = ('data_criacao',)