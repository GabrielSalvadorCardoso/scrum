from django.conf.urls import url, include
from tarefas import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    url('^$', views.api_root),
    url('^tarefas/$', views.TarefaList.as_view(), name='tarefa-list'),
    url('^tarefas/(?P<pk>[0-9]+)/$', views.TarefaDetail.as_view(), name='tarefa-detail'),
    url('^users/$', views.UserList.as_view(), name='user-list'),
    url('^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user-detail')
])

# Com format_suffix_patterns e habilitando cada view a receber
# um formato de requisição específico. Podemos fazer uma requisição
# com .json e a resposta será adequada para este caso
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]