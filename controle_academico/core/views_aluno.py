from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest

from .models import Frequencia, Nota, Turma, Aluno
from .decorators import student_required

@student_required
def home_view(request: HttpRequest):
    """
    Página inicial do aluno
    """
    
    aluno = get_object_or_404(Aluno, user=request.user)
    turmas = aluno.turmas_set.all()
    frequencias = Frequencia.objects.filter(aluno=aluno)
    notas = Nota.objects.filter(aluno=aluno)

    context = {
        'turmas': turmas,
        'frequencias': frequencias,
        'notas': notas,
    }

    return render(
        request=request, 
        template_name='aluno/home.html',
        context=context
    )


@student_required
def turma_view(request: HttpRequest, turma_id: int):
    """
    Detalhes da turma
    """

    aluno = Aluno.objects.get(user=request.user)
    turma = get_object_or_404(Turma.objects, id=turma_id, alunos__in=[aluno])
    frequencias = Frequencia.objects.filter(aluno=aluno, turma=turma).all()
    notas = Nota.objects.filter(aluno=aluno, turma=turma).all()

    context = {
        'turma': turma,
        'frequencias': frequencias,
        'notas': notas,
    }

    return render(
        request=request,
        template_name='aluno/turma.html',
        context=context
    )


@student_required
def boletim_view(request: HttpRequest, turma_id: int):
    aluno = Aluno.objects.get(user=request.user)
    turma = get_object_or_404(Turma.objects, id=turma_id, alunos__in=[aluno])
    frequencias = Frequencia.objects.filter(aluno=aluno, turma=turma).all()
    notas = Nota.objects.filter(aluno=aluno, turma=turma).all()

    context = {
        'turma': turma,
        'frequencias': frequencias,
        'notas': notas,
    }

    return render(
        request=request,
        template_name='aluno/boletim.html',
        context=context
    )
