from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from . import forms
from . import models
from .decorators import admin_required

@admin_required
def home_view(request):
    return render(request, template_name='administrador/home.html')

# -------------------------------- CRUD ALUNO ---------------------------------


@admin_required
def aluno_list_view(request):
    alunos = models.Aluno.objects.all()
    context = {'alunos': alunos}
    return render(request, template_name='administrador/aluno_list.html', context=context)


@admin_required
def aluno_details_view(request, pk: int):
    aluno = get_object_or_404(models.Aluno, pk=pk)
    context = {'aluno': aluno}
    return render(request, template_name='administrador/aluno_details.html', context=context)


@admin_required
def aluno_update_view(request, pk: int):
    pass


@admin_required
def aluno_create_view(request):
    if request.method == 'POST':
        form = forms.AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_aluno_list'))
    else:
        form = forms.AlunoForm()
    
    return render(request, 'administrador/aluno_create.html', {'form': form})


@admin_required
def aluno_delete_view(request, pk: int):
    if request.method == 'POST':
        aluno = models.Aluno.objects.get(id=pk)
        aluno.delete()
    
    return redirect(reverse('administrador_aluno_list'))

# -------------------------------- CRUD TURMA ---------------------------------

@admin_required
def turma_list_view(request):
    turmas = models.Turma.objects.all()
    context = {'turmas': turmas}
    return render(request, template_name='administrador/turma_list.html', context=context)


@admin_required
def turma_details_view(request, pk: int):
    turma = get_object_or_404(models.Turma, pk=pk)
    context = {'turma': turma}
    return render(request, template_name='administrador/turma_details.html', context=context)


@admin_required
def turma_update_view(request, pk: int):
    pass


@admin_required
def turma_create_view(request):
    if request.method == 'POST':
        form = forms.TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_turma_list'))
    else:
        form = forms.TurmaForm()
    
    return render(request, 'administrador/turma_create.html', {'form': form})


@admin_required
def turma_delete_view(request):
    pass

# -------------------------------- CRUD CURSO ---------------------------------

@admin_required
def curso_list_view(request):
    cursos = models.Curso.objects.all()
    context = {'cursos': cursos}
    return render(request, template_name='administrador/curso_list.html', context=context)


@admin_required
def curso_details_view(request, pk: int):
    curso = get_object_or_404(models.Curso, pk=pk)
    context = {'curso': curso}
    return render(request, template_name='administrador/curso_details.html', context=context)


@admin_required
def edit_curso_view(reuqest, pk: int):
    pass


@admin_required
def create_curso_view(request):
    if request.method == 'POST':
        form = forms.CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_curso_list'))
    else:
        form = forms.CursoForm()
    
    return render(request, 'administrador/curso_create.html', {'form': form})


@admin_required
def delete_curso_view(request):
    pass

# -------------------------------- CRUD DISCIPLINA ----------------------------

@admin_required
def disciplina_list_view(request):
    pass


@admin_required
def disciplina_details_view(request, pk: int):
    pass


@admin_required
def edit_disciplina_view(request, pk: int):
    pass


@admin_required
def create_disciplina_view(request):
    pass


@admin_required
def delete_disciplina_view(request):
    pass
