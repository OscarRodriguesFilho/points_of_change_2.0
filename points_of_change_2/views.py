from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.http import HttpResponse

from .models import Tarefa
from django.contrib.auth.decorators import login_required
# Create your views here.
# É aqui que ficarão as funções que você criou
from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib import messages

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
    all_notes = Tarefa.objects.filter(author=request.user.id).order_by("data")
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
        if tarefa.tipo not in lista:
            lista.append(tarefa.tipo)
    

    return render(request, 'paginas/index.html', {"tarefas": all_notes, 'pontos': pnts_tot, 'lista': lista})

@login_required
def tarefa(request, tipo):
    all_notes = Tarefa.objects.filter(author=request.user.id, tipo=tipo).order_by("data")
    todas = Tarefa.objects.filter(author=request.user.id).order_by("data")
    if request.method == 'POST':
        author = request.user
        tarefa = request.POST.get('tarefa')
        pontos = request.POST.get('pontos')
        tipo = tipo
        task = Tarefa(tarefa = tarefa, pontos = pontos, author = author, tipo = tipo)
        task.save()

    lista = []
    pnts_tot =  0
    for tarefa in all_notes:
        if tarefa.estado == 1:
            pnts_tot += tarefa.pontos
            # isso retorna a hora da tarefa
    for tarefa in todas:
        if tarefa.tipo not in lista:
            lista.append(tarefa.tipo)
    

    return render(request, 'paginas/tarefa.html', {"tarefas": all_notes, 'pontos': pnts_tot, 'lista': lista})

@login_required
def apagar(request, id_tarefa):
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, author=request.user)
    tarefa.delete()
    return redirect('index')
    
def graficos(request):
    all_notes = Tarefa.objects.filter(author=request.user.id).order_by("data")
    pnts_tot =  0
    for tarefa in all_notes:
        if tarefa.estado == 1:
            pnts_tot += tarefa.pontos
            
    return render(request, 'paginas/graficos.html', {"pontos": pnts_tot})

def estado(request, id_tarefa):
    tarefa = get_object_or_404(Tarefa, id=id_tarefa, author=request.user)
    if tarefa.estado == 0:
        tarefa.estado = 1
        tarefa.save()
    else:
        tarefa.estado = 0
        tarefa.save()
    return redirect('index')


        