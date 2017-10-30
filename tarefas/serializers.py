from rest_framework import serializers
from tarefas.models import Tarefa, TASKS_TYPES

# Serializer escrito explicitamente
"""
class TarefaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_criacao = serializers.DateTimeField()
    titulo = serializers.CharField(required=True, allow_blank=False, max_length=100)
    tipo = serializers.ChoiceField(choices=TASKS_TYPES)

    def create(self, dados_validados):
        # Criando os dados válidos no banco de dados
        return Tarefa.objects.create(**dados_validados)

    def update(self, instancia, dados_validados):
        # É feita uma comparação entre a instância que deseja-se salvar
        # e os dados já no banco da dados para saber se os novo dados são válidos
        instancia.data_criacao = dados_validados.get('data_criacao', instancia.data_criacao)
        instancia.titulo = dados_validados.get('titulo', instancia.titulo)
        instancia.tipo = dados_validados.get('tipo', instancia.tipo)
        instancia.save() # Salva as alterações se tudo estiver válido
        return instancia
"""

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ('id', 'titulo', 'data_criacao', 'tipo')