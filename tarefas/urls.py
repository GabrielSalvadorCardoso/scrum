from django.conf.urls import url
from tarefas import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url('^tarefas/$', views.TarefaList.as_view()),
    url('^tarefas/(?P<pk>[0-9]+)/$', views.TarefaDetail.as_view()),
    url('^users/$', views.UserList.as_view()),
    url('^users/(?P<pk>[0-9]+)$', views.UserDetail.as_view())
]

# Com format_suffix_patterns e habilitando cada view a receber
# um formato de requisição específico. Podemos fazer uma requisição
# com .json e a resposta será adequada para este caso
urlpatterns = format_suffix_patterns(urlpatterns)