from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.http import HttpResponse
from django.db.models import Sum
from .models import Tarefa, Novo_tipo
from django.contrib.auth.decorators import login_required
# Create your views here.
# É aqui que ficarão as funções que você criou
from django.shortcuts import render, redirect
from .forms import RegistroForm, RecomendacaoForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Recomendacao
from .forms import RecomendacaoForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Recomendacao, Like


@login_required
def like_toggle(request, recomendacao_id):
    if request.method == 'POST':
        recomendacao = Recomendacao.objects.get(id=recomendacao_id)
        like, created = Like.objects.get_or_create(
            usuario=request.user,
            recomendacao=recomendacao
        )

        if not created:
            like.delete()  # se já curtiu, descurte

        total_likes = recomendacao.likes.count()
        return JsonResponse({'likes': total_likes})




from collections import defaultdict
from django.shortcuts import render, redirect
from .models import Recomendacao
from .forms import RecomendacaoForm
import unicodedata

def slug_categoria(categoria):
    # Remove acentos, converte para minúsculo e tira espaços extras
    categoria = unicodedata.normalize('NFKD', categoria).encode('ASCII', 'ignore').decode('ASCII')
    return categoria.strip().lower()

def recomendacoes_unificadas_view(request):
    if request.method == 'POST':
        form = RecomendacaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recomendacoes')
    else:
        form = RecomendacaoForm()

    cards = Recomendacao.objects.all().order_by('-data_publicacao')
    categorias = defaultdict(list)

    for card in cards:
        chave_normalizada = slug_categoria(card.categoria)
        categorias[chave_normalizada].append(card)

    # Agora, crie um dicionário que preserve o nome original da categoria para exibição
    categorias_exibicao = {}
    for chave, cards_lista in categorias.items():
        nome_original = cards_lista[0].categoria  # nome original para exibição no HTML
        categorias_exibicao[nome_original] = cards_lista

    return render(request, 'paginas/recomendacoes.html', {
        'categorias': categorias_exibicao,
        'form': form
    })





def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')  # nome da sua view de login
    else:
        form = RegistroForm()
    return render(request, 'paginas/registro.html', {'form': form})

        

@login_required
def index(request):
    # isso pega todas as tarefas
    all_notes = Tarefa.objects.filter(author=request.user.id).order_by("estado")
    
    if request.method == 'POST':
        author = request.user
        tarefa = request.POST.get('tarefa')
        pontos = request.POST.get('pontos')
        task = Tarefa(tarefa = tarefa, pontos = pontos, author = author)
        task.save()
   
    lista = []
    pnts_tot =  0
    for tarefa in all_notes:
        if tarefa.estado == 1:
            pnts_tot += tarefa.pontos
            # isso retorna a hora da tarefa
        
    
    tipos = Novo_tipo.objects.filter(author=request.user.id)
    for tipo in tipos:
        lista.append(tipo.nome)
    
        
      
    return render(request, 'paginas/index.html', {"tarefas": all_notes, 'pontos': pnts_tot, 'lista': lista})

@login_required
def tarefa(request, tipo):
    all_notes = Tarefa.objects.filter(author=request.user.id, tipo=tipo).order_by('estado')
    todas = Tarefa.objects.filter(author=request.user.id).order_by("-data")
    if request.method == 'POST':
        author = request.user
        tarefa = request.POST.get('tarefa')
        pontos = request.POST.get('pontos')
        tipo = tipo
        task = Tarefa(tarefa = tarefa, pontos = pontos, author = author, tipo = tipo)
        task.save()
   
    p = Novo_tipo.objects.filter(nome=tipo, author = request.user).first()
    if p is None:
        # não existe — define um valor padrão
        meta = None
    else:
        meta = p.meta
    
    lista = []
    pnts_tot =  0
    for tarefa in all_notes:
        if tarefa.estado == 1:
            pnts_tot += tarefa.pontos
            # isso retorna a hora da tarefa
    for tarefa in todas:
        if tarefa.tipo not in lista:
            if tarefa.tipo == 'i':
                tarefa.tipo = 'Avulso'
            lista.append(tarefa.tipo)
    

    return render(request, 'paginas/tarefa.html', {"tarefas": all_notes, 'pontos': pnts_tot, 'lista': lista, 'meta': meta, 'tipo': tipo})

@login_required
def recomendacoes(request):
    todas = Tarefa.objects.filter(author=request.user.id).order_by("-data")
    lista = []
    for tarefa in todas:
        if tarefa.tipo not in lista:
            if tarefa.tipo == 'i':
                tarefa.tipo = 'Avulso'
            lista.append(tarefa.tipo)
    return render(request,'paginas/recomendacoes.html', {'lista': lista})

@login_required
def nova_tarefa(request):
    if request.method == 'POST':
        author = request.user
        nome = request.POST.get('nome')
        meta = request.POST.get('meta')
        novo_tipo = Novo_tipo(nome = nome, meta = meta, author = author)
        novo_tipo.save()
        return redirect('index')

    lista = []
    
    tipos = Novo_tipo.objects.filter(author=request.user.id)
    for tipo in tipos:
        if tipo.nome == 'i':
            tipo.nome = 'Avulso'
        lista.append(tipo.nome)
        

    return render(request, 'paginas/nova_tarefa.html', {'lista': lista})

@login_required
def apagar(request, id_tarefa):
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, author=request.user)
    tipo = tarefa.tipo
    tarefa.delete()
    url = '/tipo/' + tipo
    return redirect(url)
    
@login_required
def graficos(request): 
   
    qs = Tarefa.objects.filter(author=request.user, estado=1).values('tipo').annotate(total=Sum('pontos')).order_by('tipo')
    
    labels = [
        'Avulso' if item['tipo'] == 'i' else item['tipo']
        for item in qs
    ]
    data = [item['total'] for item in qs]

    return render(request, 'paginas/graficos.html', {
        'labels': labels,
        'data':   data,
    })

@login_required
def estado(request, id_tarefa):
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, author=request.user)
    if tarefa.estado == 0:
        tarefa.estado = 1
        tarefa.save()
    else:
        tarefa.estado = 0
        tarefa.save()
    tipo = tarefa.tipo
    url = '/tipo/' + tipo
    return redirect(url)


        