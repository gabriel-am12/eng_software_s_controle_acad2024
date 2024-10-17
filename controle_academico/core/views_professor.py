from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest

from .decorators import teacher_required
from .models import Professor, Atividade, Turma
from .forms import AtividadeForm, NoticiaForm

@teacher_required
def home_view(request: HttpRequest):
    user = request.user
    professor = Professor.objects.get(user=user)
    
    context = {
        'turmas': professor.turmas.all(),
    }

    return render(
        request=request,
        template_name='professor/home.html',
        context=context
    )


@teacher_required
def turma_list_view(request):
    pass


@teacher_required
def turma_details_view(request: HttpRequest, turma_id: int):
    user = request.user
    professor = Professor.objects.get(user=user)
    
    context = {
        'turma': professor.turmas.get(id=turma_id),
    }

    return render(
        request=request,
        template_name='professor/turma_details.html',
        context=context
    )


@teacher_required
def turma_atividade_list_view(request: HttpRequest, turma_id: int):
    user = request.user
    professor = Professor.objects.get(user=user)
    
    context = {
        'turma': professor.turmas.get(id=turma_id),
    }

    return render(
        request=request,
        template_name='professor/turma_atividade_list.html',
        context=context
    )


@teacher_required
def registrar_notas_view(request, turma_id: int):
    turma = Turma.objects.get(id=turma_id)
    
    context = {
        'turma': turma,
        'alunos': turma.alunos.all(),
    }

    return render(
        request=request,
        template_name='professor/registrar_nota.html',
        context=context
    )


@teacher_required
def registrar_frequencia_view(request, turma_id: int):
    turma = Turma.objects.get(id=turma_id)
    
    context = {
        'turma': turma,
        'alunos': turma.alunos.all(),
    }

    return render(
        request=request,
        template_name='professor/registrar_frequencia.html',
        context=context
    )

# -----------------------------------------------------------------------------

@teacher_required
def atividade_details_view(request: HttpRequest, atividade_id: int):
    pass


@teacher_required
def atividade_create_view(request: HttpRequest):
    form = None

    if request.POST:
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade: Atividade = form.save()
            
            return redirect(reverse_lazy('professor_turma_atividade_list', args=[atividade.turma.pk]))
    else:    
        form = AtividadeForm()

    return render(
        request,
        template_name='professor/atividade_create.html',
        context={
            'form': form
        }        
    )


@teacher_required
def atividade_delete_view(request: HttpRequest, atividade: int):
    pass

# -----------------------------------------------------------------------------

@teacher_required
def noticia_create_view(request: HttpRequest, turma_id: int):
    form = None

    if request.POST:
        form = NoticiaForm(request.POST)
        if form.is_valid():
            noticia = form.save()
            return redirect(reverse_lazy('professor_turma_details', args=[turma_id]))
    else:   
        form = NoticiaForm()

    return render(
        request,
        template_name='professor/generic_form.html',
        context={
            'page_title': 'Cadastrar notícia',  
            'form': form
        }        
    )

