from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest

from .decorators import teacher_required
from .models import Professor, Atividade, Turma
from .forms import AtividadeForm

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

# class RegistrarFrequenciaView(View):
#     def get(self, request, turma_id):
#         turma = Turma.objects.get(id=turma_id)
#         alunos = turma.alunos.all()
#         frequencias = Frequencia.objects.filter(turma=turma)
#         form = FrequenciaForm()
#         context = {'turma': turma, 'alunos': alunos, 'frequencias': frequencias ,'form': form}
#         return render(request, 'registrar_frequencia.html', context)

#     def post(self, request, turma_id):
#         turma = Turma.objects.get(id=turma_id)
#         alunos = turma.alunos.all()
#         data = request.POST.get('data')
#         for aluno in alunos:
#             presente = request.POST.get(f'presente_{aluno.id}') is not None
#             frequencia, created = Frequencia.objects.update_or_create(
#                 aluno=aluno,
#                 turma=turma,
#                 data=data,
#                 defaults={'presente': presente}
#             )
#             return redirect('professor_inicio')
#         return render(request, 'registrar_frequencia.html', {'turma': turma, 'alunos': turma.alunos.all(), 'form': form})

# class RegistrarNotaView(View):
#     def get(self, request, turma_id):
#         turma = Turma.objects.get(id=turma_id)
#         alunos = turma.alunos.all()
#         notas = Nota.objects.filter(turma=turma)
        
#         context = {
#             'turma': turma,
#             'alunos': alunos,
#             'notas': notas
#         }
        
#         return render(request, 'registrar_nota.html', context)

#     def post(self, request, turma_id):
#         turma = Turma.objects.get(id=turma_id)
#         alunos = turma.alunos.all()

#         for aluno in alunos:
#             avaliacao = request.POST.get(f'avaliacao_{aluno.id}')
#             nota_valor = request.POST.get(f'nota_{aluno.id}')

#             if avaliacao and nota_valor:
#                 nota, created = Nota.objects.get_or_create(
#                     aluno=aluno,
#                     turma=turma,
#                     avaliacao=avaliacao,
#                     defaults={'nota': nota_valor}
#                 )
#                 if not created:
#                     nota.nota = nota_valor
#                     nota.save()
#         return redirect('registrar_nota', turma_id=turma.id)

# class TeacherAdicionarRemoverEstudantesView(View):
#     def get(self, request, turma_id):
#         turma = get_object_or_404(Turma, id=turma_id)
#         alunos = Aluno.objects.all()
#         alunos_turma = turma.alunos.all()  

#         context = {
#             'turma': turma,
#             'alunos': alunos,
#             'alunos_turma': alunos_turma
#         }
#         return render(request, 'gerenciar_estudantes.html', context)

#     def post(self, request, turma_id):
#         turma = get_object_or_404(Turma, id=turma_id)
#         selected_students = request.POST.getlist('alunos')  # Obtém os alunos selecionados
#         turma.alunos.set(selected_students)
#         turma.save()
#         return redirect('professor_inicio')
