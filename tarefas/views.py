#from django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
from tarefas.models import Tarefa
from tarefas.serializers import TarefaSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
