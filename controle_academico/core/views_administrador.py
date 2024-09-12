from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from . import forms
from . import models

def home_view(request):
    return render(request, template_name='administrador/home.html')

# -------------------------------- CRUD ALUNO ---------------------------------

def aluno_list_view(request):
    alunos = models.Aluno.objects.all()
    context = {'alunos': alunos}
    return render(request, template_name='administrador/aluno_list.html', context=context)


def aluno_details_view(request, pk: int):
    aluno = get_object_or_404(models.Aluno, pk=pk)
    context = {'aluno': aluno}
    return render(request, template_name='administrador/aluno_details.html', context=context)


def aluno_update_view(request, pk: int):
    pass


def aluno_create_view(request):
    if request.method == 'POST':
        form = forms.AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_aluno_list'))
    else:
        form = forms.AlunoForm()
    
    return render(request, 'administrador/aluno_create.html', {'form': form})



def aluno_delete_view(request, pk: int):
    pass

# -------------------------------- CRUD TURMA ---------------------------------

def turma_list_view(request):
    turmas = models.Turma.objects.all()
    context = {'turmas': turmas}
    return render(request, template_name='administrador/turma_list.html', context=context)


def turma_details_view(request, pk: int):
    turma = get_object_or_404(models.Turma, pk=pk)
    context = {'turma': turma}
    return render(request, template_name='administrador/turma_details.html', context=context)


def turma_update_view(request, pk: int):
    pass


def turma_create_view(request):
    if request.method == 'POST':
        form = forms.TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_turma_list'))
    else:
        form = forms.TurmaForm()
    
    return render(request, 'administrador/turma_create.html', {'form': form})


def turma_delete_view(request):
    pass

# -------------------------------- CRUD CURSO ---------------------------------

def curso_list_view(request):
    pass


def curso_details_view(request, pk: int):
    pass


def edit_curso_view(reuqest, pk: int):
    pass


def create_curso_view(request):
    pass


def delete_curso_view(request):
    pass

# -------------------------------- CRUD DISCIPLINA ----------------------------

def disciplina_list_view(request):
    pass

def disciplina_details_view(request, pk: int):
    pass


def edit_disciplina_view(request, pk: int):
    pass


def create_disciplina_view(request):
    pass


def delete_disciplina_view(request):
    pass
