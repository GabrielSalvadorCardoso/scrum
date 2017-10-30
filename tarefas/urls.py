from django.conf.urls import url
from tarefas import views

urlpatterns = [
    url('^tarefas/$', views.tarefa_list),
    url('^tarefas/(?P<pk>[0-9]+)/$', views.tarefa_detail)
]