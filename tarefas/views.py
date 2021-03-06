#from django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
from tarefas.models import Tarefa
from django.contrib.auth.models import User
from tarefas.serializers import TarefaSerializer, UserSerializer
#from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
#from rest_framework.views import APIView
#from django.http import Http404
#from rest_framework import mixins
from rest_framework import generics, permissions
from tarefas.permissions import IsOwnerOrReadOnly

# Views baseadas em funções
"""
#@csrf_exempt # Esta função é isenta de token csrf
# Esta será uma view baseada em função que tratará requisições GET e POST
@api_view(['GET', 'POST'])
def tarefa_list(request, format=None):
    if request.method == 'GET':
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        # Agora a resposta é de acordo com a requisição e não mais um JSON
        return Response(serializer.data)
        #return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        # O objeto Request do Rest Framework torna o parsing
        # mais flexivel pois elimina a necessidade do parser
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return JsonResponse(serializer.data, status=201)
        # Agora os códigos de erro são mais descritivos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return JsonResponse(serializer.errors, status=400)

#@csrf_exempt
# Com format a view tem a possibilidade de
# receber um tipo de requisição especifica como JSON
@api_view(['GET', 'PUT', 'DELETE'])
def tarefa_detail(request, pk, format=None):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
    except Tarefa.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        #return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data)
        #return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = TarefaSerializer(tarefa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            #return JsonResponse(serializer.data)
        #return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        #return HttpResponse(status=204)
"""

# Qualquer requisição feita para a raiz do projeto terá uma lista de urls para as views
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user': reverse('user-list', request=request, format=format),
        'tarefas': reverse('tarefa-list', request=request, format=format)
    })

# Views baseadas em classes
"""
class TarefaList(APIView):
    def get(self, request, format=None):
        tarefas = Tarefa.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TarefaDetail(APIView):
    def get_object(self, pk):
        try:
            tarefa = Tarefa.objects.get(pk=pk)
        except Tarefa.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        tarefa = self.get_object(pk)
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tarefa = self.get_object(pk)
        # Neste caso o serializer recebe tanto o objeto do banco quanto o dado enviado na requisição
        serializer = TarefaSerializer(tarefa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tarefa = self.get_object(pk)
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# Views baseadas em Mixins
# Cada um dos Mixins provê uma ação como Create, List, Destroy, etc
# A classe(view) que herda de uma deste Mixins conterá uma determinada ação
"""
class TarefaList(mixins.ListModelMixin, # Mixin responsável pela listagem
                  mixins.CreateModelMixin, # Mixin responsável pela criação
                  generics.GenericAPIView):
    queryset = Tarefa.objects.all() # Como obter os recursos do banco de dados
    serializer_class = TarefaSerializer # Classe serializer deste recurso

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TarefaDetail(mixins.RetrieveModelMixin, # Provê ação de recuperação de um recurso
                   mixins.UpdateModelMixin, # Provê ação de atualização
                   mixins.DestroyModelMixin, # Provê ação de deleção
                   generics.GenericAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

# Views baseadas em view genericas
"""
class TarefaList(generics.ListCreateAPIView): # Provê ações de criação e listagem
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        # Sobrescrevendo 'perform_create' podemos controlar como
        # a instancia de Tarefa será salvo. Por exemplo, podemos
        # associar o usuario referente a esta requisição a intância
        # de Tarefa. Agora o serializer deste modelo pode validar
        # também este campo
        serializer.save(criador=self.request.user)
        # Agora todas as requisições que quiserem executar uma ação de
        # criação, deleção ou alteração deverão ser autenticadas. Do contrário
        # apenas terão permissão de leitura
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                              IsOwnerOrReadOnly)

class TarefaDetail(generics.RetrieveUpdateDestroyAPIView): # Provê ações de recuperação, atualização e destruição
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""

# Views baseadas em ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet): # Apenas as operaçãoes de leitura para esta view
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(criador=self.request.user)