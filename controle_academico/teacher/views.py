from django.shortcuts import render, redirect
from django.views.generic import View

from core.models import Turma
from .forms import FrequenciaForm, NotaForm

# Create your views here.
class TeacherDashboardView(View):
    def get(self, request):
        professor = request.user.professor  
        turmas = Turma.objects.filter(professores=professor)
        context = {'turmas': turmas}
        return render(request, 'teacher/teacher_dashboard.html', context)


class RegistrarFrequenciaView(View):
    def get(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        form = FrequenciaForm()
        context = {'turma': turma, 'alunos': alunos, 'form': form}
        return render(request, 'teacher/registrar_frequencia.html', context)

    def post(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        form = FrequenciaForm(request.POST)
        if form.is_valid():
            for aluno in turma.alunos.all():
                frequencia = form.save(commit=False)
                frequencia.aluno = aluno
                frequencia.turma = turma
                frequencia.save()
            #return redirect(reverse('turma_detail', args=[turma_id]))
            return redirect('teacher_dashboard')
        return render(request, 'teacher/registrar_frequencia.html', {'turma': turma, 'alunos': turma.alunos.all(), 'form': form})


class RegistrarNotaView(View):
    def get(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        form = NotaForm()
        context = {'turma': turma, 'alunos': alunos, 'form': form}
        return render(request, 'registrar_nota.html', context)

    def post(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        form = NotaForm(request.POST)
        if form.is_valid():
            for aluno in turma.alunos.all():
                nota = form.save(commit=False)
                nota.aluno = aluno
                nota.turma = turma
                nota.save()
            #return redirect('detalhes_turma', turma_id=turma.id)
            return redirect('teacher_dashboard')
        return render(request, 'registrar_nota.html', {'form': form, 'turma': turma})
