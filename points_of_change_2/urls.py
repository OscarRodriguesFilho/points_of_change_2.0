from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('anotacoes/<int:id_tarefa>/apagar', views.apagar, name='apagar'),
    path('anotacoes/<int:id_tarefa>/estado', views.estado, name='estado'),
    path('tipo/<str:tipo>/', views.tarefa, name='tarefa'),
    path('graficos/', views.graficos, name='graficos'),
    path('registro/', views.registro, name='registro'),
    path('nova_tarefa/', views.nova_tarefa, name='nova_tarefa'),
    path('recomendacao/<int:recomendacao_id>/like/', views.like_toggle, name='like_toggle'),
    # path('recomendacoes/', views.recomendacoes, name='recomendacoes'),
    path('recomendacoes/', views.recomendacoes_unificadas_view, name='recomendacoes'),
    path('', views.index, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
