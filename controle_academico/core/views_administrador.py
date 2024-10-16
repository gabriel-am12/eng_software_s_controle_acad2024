from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from . import forms
from . import models
from .decorators import admin_required

@admin_required
def home_view(request):
    return render(request, template_name='administrador/home.html')

# -------------------------------- CRUD ALUNO ---------------------------------

@admin_required
def aluno_list_view(request: HttpRequest):
    q = request.GET.get('q')

    if q is None:
        alunos = models.Aluno.objects.all()
    else:
        alunos = models.Aluno.objects.filter(nome__contains=q)
        
    context = {
        'page_title': 'Lista de alunos',
        'add_link': reverse('administrador_aluno_create'),
        'alunos': alunos, 
    }
    return render(request, template_name='administrador/aluno_list.html', context=context)


@admin_required
def aluno_details_view(request: HttpRequest, pk: int):
    aluno = get_object_or_404(models.Aluno, pk=pk)
    context = {'aluno': aluno}
    return render(request, template_name='administrador/aluno_details.html', context=context)


@admin_required
def aluno_update_view(request: HttpRequest, pk: int):
    pass


@admin_required
def aluno_create_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.AlunoForm(request.POST)
        
        if form.is_valid():
            data = form.clean()
            
            user = get_user_model().objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )
            user.save()

            perfil = models.Perfil.objects.create(
                user=user,
                user_type='student'
            )
            perfil.save()

            aluno = form.save()
            aluno.user = user
            aluno.profile = perfil
            aluno.save()
            
            return redirect(reverse('administrador_aluno_list'))
    else:
        form = forms.AlunoForm()
    
    context = {
        'page_title': 'Cadastrar aluno',
        'form': form
    }

    return render(request, 'administrador/generic_form.html', context)


@admin_required
def aluno_delete_view(request: HttpRequest, pk: int):
    if request.method == 'POST':
        aluno = models.Aluno.objects.get(id=pk)
        aluno.user.delete()
    
    return redirect(reverse('administrador_aluno_list'))

# ------------------------------ CRUD PROFESSOR -------------------------------

@admin_required
def professor_list_view(request: HttpRequest):
    q = request.GET.get('q')

    if q is None:
        professores = models.Professor.objects.all()
    else:
        professores = models.Professor.objects.filter(nome__contains=q)
        
    context = {
        'page_title': 'Lista de professores',
        'add_link': reverse('administrador_professor_create'),
        'professores': professores, 
    }
    return render(request, template_name='administrador/professor_list.html', context=context)


@admin_required
def professor_details_view(request: HttpRequest, pk: int):
    professor = get_object_or_404(models.Professor, pk=pk)
    context = {'professor': professor}
    return render(request, template_name='administrador/professor_details.html', context=context)


@admin_required
def professor_update_view(request: HttpRequest, pk: int):
    pass


@admin_required
def professor_create_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.ProfessorForm(request.POST)
        
        if form.is_valid():
            data = form.clean()
            
            user = get_user_model().objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )
            user.save()

            perfil = models.Perfil.objects.create(
                user=user,
                user_type='teacher'
            )
            perfil.save()

            professor = form.save()
            professor.user = user
            professor.profile = perfil
            professor.save()
            
            return redirect(reverse('administrador_professor_list'))
    else:
        form = forms.ProfessorForm()
    
    context = {
        'page_title': 'Cadastrar professor',
        'form': form
    }

    return render(request, 'administrador/generic_form.html', context)


@admin_required
def professor_delete_view(request: HttpRequest, pk: int):
    if request.method == 'POST':
        prof = models.Professor.objects.get(id=pk)
        prof.user.delete()
    
    return redirect(reverse('administrador_professor_list'))


# -------------------------------- CRUD TURMA ---------------------------------

@admin_required
def turma_list_view(request: HttpRequest):
    q = request.GET.get('q')

    if q is None:
        turmas = models.Turma.objects.all()
    else:
        turmas = models.Turma.objects.filter(disciplina__nome__contains=q)

    context = {
        'page_title': 'Lista de turmas',
        'add_link': reverse('administrador_turma_create'),
        'turmas': turmas
    }
    return render(request, template_name='administrador/turma_list.html', context=context)


@admin_required
def turma_details_view(request: HttpRequest, pk: int):
    turma = get_object_or_404(models.Turma, pk=pk)
    context = {'turma': turma}
    return render(request, template_name='administrador/turma_details.html', context=context)


@admin_required
def turma_update_view(request: HttpRequest, pk: int):
    pass


@admin_required
def turma_create_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_turma_list'))
    else:
        form = forms.TurmaForm()
    
    context = {
        'page_title': 'Cadastrar turma',
        'form': form
    }

    return render(request, 'administrador/generic_form.html', context)


@admin_required
def turma_delete_view(request: HttpRequest, pk: int):
    if request.method == 'POST':
        turma = models.Turma.objects.get(id=pk)
        turma.delete()
    
    return redirect(reverse('administrador_turma_list'))

# -------------------------------- CRUD CURSO ---------------------------------

@admin_required
def curso_list_view(request: HttpRequest):
    cursos = models.Curso.objects.all()
    context = {
        'page_title': 'Lista de cursos',
        'add_link': reverse('administrador_curso_create'),
        'cursos': cursos
    }
    return render(request, template_name='administrador/curso_list.html', context=context)


@admin_required
def curso_details_view(request: HttpRequest, pk: int):
    curso = get_object_or_404(models.Curso, pk=pk)
    context = {'curso': curso}
    return render(request, template_name='administrador/curso_details.html', context=context)


@admin_required
def edit_curso_view(reuqest: HttpRequest, pk: int):
    pass


@admin_required
def create_curso_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_curso_list'))
    else:
        form = forms.CursoForm()
    
    context = {
        'page_title': 'Cadastrar curso',
        'form': form
    }

    return render(request, 'administrador/generic_form.html', context)


@admin_required
def delete_curso_view(request: HttpRequest, pk: int):
    if request.method == 'POST':
        curso = models.Curso.objects.get(id=pk)
        curso.delete()
    
    return redirect(reverse('administrador_turma_list'))

# -------------------------------- CRUD DISCIPLINA ----------------------------

@admin_required
def disciplina_list_view(request: HttpRequest):
    disciplinas = models.Disciplina.objects.all()
    context = {
        'page_title': 'Lista de disciplinas',
        'add_link': reverse('administrador_disciplina_create'),
        'disciplinas': disciplinas
    }
    return render(request, template_name='administrador/disciplina_list.html', context=context)


@admin_required
def disciplina_details_view(request: HttpRequest, pk: int):
    pass


@admin_required
def edit_disciplina_view(request: HttpRequest, pk: int):
    pass


@admin_required
def create_disciplina_view(request: HttpRequest):
    if request.method == 'POST':
        form = forms.DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('administrador_disciplina_list'))
    else:
        form = forms.DisciplinaForm()
    
    context = {
        'page_title': 'Cadastrar disciplina',
        'form': form
    }

    return render(request, 'administrador/generic_form.html', context)


@admin_required
def delete_disciplina_view(request: HttpRequest, pk: int):
    if request.method == 'POST':
        turma = models.Disciplina.objects.get(id=pk)
        turma.delete()
    
    return redirect(reverse('administrador_disciplina_list'))
