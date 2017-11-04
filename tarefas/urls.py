from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from tarefas import views
#from tarefas.views import TarefaViewSet, UserViewSet, api_root
#from rest_framework.urlpatterns import format_suffix_patterns

# Ligando as urls as ações correspondentes dentro das views
"""
tarefa_list = TarefaViewSet.as_view({
    # método: ação
    'get': 'list',
    'post': 'create'
})

tarefa_detail = TarefaViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# Com format_suffix_patterns e habilitando cada view a receber
# um formato de requisição específico. Podemos fazer uma requisição
# com .json e a resposta será adequada para este caso
urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^tarefas/$', tarefa_list, name='tarefa-list'),
    url(r'^tarefas/(?P<pk>[0-9]+)/$', tarefa_detail, name='tarefa-detail'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
])

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
"""

# O DefaultRouter ainda provê uma url padrão para o API root
router = DefaultRouter()
router.register(r'tarefas', views.TarefaViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # Mapeando as urls criadas acima
    url(r'^', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]