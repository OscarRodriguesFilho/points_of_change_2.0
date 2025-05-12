from django.urls import path

from . import views


urlpatterns = [
    path('anotacoes/<int:id_tarefa>/apagar', views.apagar, name='apagar'),
    path('anotacoes/<int:id_tarefa>/estado', views.estado, name='estado'),
    path('graficos/', views.graficos, name='graficos'),
    path('registro/', views.registro, name='registro'),
    path('', views.index, name='index'),
    
]