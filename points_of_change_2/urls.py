from django.urls import path

from . import views


urlpatterns = [
    path('anotacoes/<int:id_tarefa>/apagar', views.apagar, name='apagar'),
    path('anotacoes/<int:id_tarefa>/estado', views.estado, name='estado'),
    path('tipo/<str:tipo>/', views.tarefa, name='tarefa'),
    path('graficos/', views.graficos, name='graficos'),
    path('registro/', views.registro, name='registro'),
    path('nova_tarefa/', views.nova_tarefa, name='nova_tarefa'),
    path('recomendacoes/', views.recomendacoes, name='recomendacoes'),
    path('', views.index, name='index'),
]
