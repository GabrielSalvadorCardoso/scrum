from django.db import models

TASKS_TYPES = [('Desenvolvimneto','Desenvolvimento'),
               ('Modelagem', 'Modelagem'),
               ('Engenharia de Requisitos', 'Engenharia de Requisitos'),
               ('Omologação', 'Omologação'),('Testes', 'Testes')]

class Tarefa(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=100, blank=False)
    tipo = models.CharField(choices=TASKS_TYPES, max_length=100)
    # SINTAXE: ForeignKey(classe_relacionada, nome_foreign_key_reversa, acao_quando_deletar)
    # Neste caso a foreign key reversa será um atributo que guardará todas as tarefas a qual um usuário esta relacionado
    criador = models.ForeignKey('auth.User', related_name='tarefas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('data_criacao',)