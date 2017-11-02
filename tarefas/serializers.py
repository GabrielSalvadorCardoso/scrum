from rest_framework import serializers
from tarefas.models import Tarefa, TASKS_TYPES
from django.contrib.auth.models import User

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
    # O argumento 'source' controla qual atributo será usado para ppopular
    # o campo 'criador' na versão serializada de uma instância de Tarefa
    criador = serializers.ReadOnlyField(source='criador.username')

    class Meta:
        model = Tarefa
        fields = ('id', 'titulo', 'data_criacao', 'tipo', 'criador')

class UserSerializer(serializers.ModelSerializer):
    # Devemos adicionar expicitamente qualquer campo referente a um relacionamento reverso
    # pois o serializer não faz isso automaticamente.
    # PrimaryKeyRelatedFiels, neste caso, representa um relacionamenteo reverso
    # que foi escrito no modelo da tarefa como "related_name='tarefas'"
    tarefas = serializers.PrimaryKeyRelatedField(many=True, queryset=Tarefa.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'tarefas')