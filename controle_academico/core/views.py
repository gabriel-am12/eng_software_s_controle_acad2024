from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Profile, Curso, Disciplina, Turma, Aluno, Professor, Frequencia, Nota
from .forms import SignUpForm, CursoForm, DisciplinaForm, TurmaForm, FrequenciaForm, NotaForm, TeacherAdicionarRemoverEstudantesForm
from reportlab.pdfgen import canvas

# Redirect, Registro e Login
def redirect_user_based_on_type(user):
    if user.profile.user_type == 'student':
        return redirect('student_dashboard')
    elif user.profile.user_type == 'teacher':
        return redirect('teacher_dashboard')
    elif user.profile.user_type == 'administrator':
        return redirect('administrator_dashboard')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_based_on_type(user)
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user_based_on_type(user)
        else:
            return render(request, 'login.html', {'error': 'Username ou senha inválidos'})
    return render(request, 'login.html')

# Estudante, Professor e Administrador
class StudentDashboardView(View):
    def get(self, request, *args, **kwargs):
        aluno = get_object_or_404(Aluno, user=request.user)
        turmas = aluno.turmas_set.all()
        frequencias = Frequencia.objects.filter(aluno=aluno)
        notas = Nota.objects.filter(aluno=aluno)


        print(f"Turmas do aluno {aluno.user.username}: {turmas}")
        print(f"Frequências do aluno: {frequencias}")
        print(f"Notas do aluno: {notas}")

        context = {
            'turmas': turmas,
            'frequencias': frequencias,
            'notas': notas,
        }
        return render(request, 'student_dashboard.html', context)

class TeacherDashboardView(View):
    def get(self, request):
        professor = request.user.professor  
        turmas = Turma.objects.filter(professores=professor)  
        alunos = Aluno.objects.filter(turmas_set__in=turmas).distinct()  
        context = {'turmas': turmas, 'alunos': alunos}
        return render(request, 'teacher_dashboard.html', context)

class AdministratorDashboardView(View):
    def get(self, request):
        alunos = Aluno.objects.all()
        context = {
            'alunos': alunos,
        }
        return render(request, 'administrator_dashboard.html', context)


# Curso, Turma e Disciplina
class CursoListView(ListView):
    model = Curso
    template_name = 'curso_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CursoForm()  
        return context

    def post(self, request, *args, **kwargs):
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curso_list')
        return self.get(request, *args, **kwargs)

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso_detail.html'

    def post(self, request, *args, **kwargs):
        curso = self.get_object()
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('curso_detail', pk=curso.pk)
        return render(request, self.template_name, {'object': curso, 'form': form})

class DisciplinaListView(ListView):
    model = Disciplina
    template_name = 'disciplina_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DisciplinaForm()  
        return context

    def post(self, request, *args, **kwargs):
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disciplina_list')
        return self.get(request, *args, **kwargs)

class DisciplinaDetailView(DetailView):
    model = Disciplina
    template_name = 'disciplina_detail.html'

    def post(self, request, *args, **kwargs):
        disciplina = self.get_object()
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('disciplina_detail', pk=disciplina.pk)
        return render(request, self.template_name, {'object': disciplina, 'form': form})

class TurmaListView(ListView):
    model = Turma
    template_name = 'turma_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TurmaForm()
        context['alunos'] = Aluno.objects.all()  
        context['professores'] = Professor.objects.all()  
        return context

    def post(self, request, *args, **kwargs):
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turma_list')
        return self.get(request, *args, **kwargs)

class TurmaDetailView(DetailView):
    model = Turma
    template_name = 'turma_detail.html'

    def post(self, request, *args, **kwargs):
        turma = self.get_object()
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('turma_detail', pk=turma.pk)
        return render(request, self.template_name, {'object': turma , 'form': form})

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

class DisciplinaDeleteView(DeleteView):
    model = Disciplina
    template_name = 'disciplina_confirm_delete.html'
    success_url = reverse_lazy('disciplina_list')

class TurmaDeleteView(DeleteView):
    model = Turma
    template_name = 'turma_confirm_delete.html'
    success_url = reverse_lazy('turma_list')

# Frequência e Nota - teacher_dashboard

class RegistrarFrequenciaView(View):
    def get(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        frequencias = Frequencia.objects.filter(turma=turma)
        form = FrequenciaForm()
        context = {'turma': turma, 'alunos': alunos, 'frequencias': frequencias ,'form': form}
        return render(request, 'registrar_frequencia.html', context)

    def post(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        data = request.POST.get('data')
        for aluno in alunos:
            presente = request.POST.get(f'presente_{aluno.id}') is not None
            frequencia, created = Frequencia.objects.update_or_create(
                aluno=aluno,
                turma=turma,
                data=data,
                defaults={'presente': presente}
            )
            return redirect('teacher_dashboard')
        return render(request, 'registrar_frequencia.html', {'turma': turma, 'alunos': turma.alunos.all(), 'form': form})

class RegistrarNotaView(View):
    def get(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        notas = Nota.objects.filter(turma=turma)
        
        context = {
            'turma': turma,
            'alunos': alunos,
            'notas': notas
        }
        
        return render(request, 'registrar_nota.html', context)

    def post(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()

        for aluno in alunos:
            avaliacao = request.POST.get(f'avaliacao_{aluno.id}')
            nota_valor = request.POST.get(f'nota_{aluno.id}')

            if avaliacao and nota_valor:
                nota, created = Nota.objects.get_or_create(
                    aluno=aluno,
                    turma=turma,
                    avaliacao=avaliacao,
                    defaults={'nota': nota_valor}
                )
                if not created:
                    nota.nota = nota_valor
                    nota.save()
        return redirect('registrar_nota', turma_id=turma.id)

class TeacherAdicionarRemoverEstudantesView(View):
    def get(self, request, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        alunos = Aluno.objects.all()
        alunos_turma = turma.alunos.all()  

        context = {
            'turma': turma,
            'alunos': alunos,
            'alunos_turma': alunos_turma
        }
        return render(request, 'gerenciar_estudantes.html', context)

    def post(self, request, turma_id):
        turma = get_object_or_404(Turma, id=turma_id)
        selected_students = request.POST.getlist('alunos')  # Obtém os alunos selecionados
        turma.alunos.set(selected_students)
        turma.save()
        return redirect('teacher_dashboard')

# Relatórios / Boletins
class RelatorioAlunoView(View):
    def get(self, request, aluno_id):
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        turmas = Turma.objects.filter(alunos=aluno).select_related('disciplina__curso')
        notas = Nota.objects.filter(aluno=aluno)
        frequencias = Frequencia.objects.filter(aluno=aluno)
        
        previous_url = request.META.get('HTTP_REFERER', '/teacher_dashboard')

        context = {
            'aluno': aluno,
            'turmas': turmas,
            'notas': notas,
            'frequencias': frequencias,
            'redirect_url': previous_url,
        }

        return render(request,'relatorio_aluno.html', context)
    
def gerar_relatorio_pdf(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    
    # Criação de uma resposta HTTP com o tipo de conteúdo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{aluno.nome}.pdf"'
    
    # Criação do objeto Canvas para o PDF
    p = canvas.Canvas(response)
    
    # Título do relatório
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Relatório de Desempenho - {aluno.nome}")
    
    # Dados do aluno
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Nome: {aluno.nome}")
    p.drawString(100, 750, f"Matricula: {aluno.matricula}")
    p.drawString(100, 730, f"Email: {aluno.email}")
    
    # Adicionar turmas e professores
    turmas = aluno.turmas.all()
    p.drawString(100, 700, "Cursos, Disciplinas e Turmas:")
    altura = 680
    for turma in turmas:
        professores = ', '.join([professor.user.username for professor in turma.professores.all()])
        p.drawString(120, altura, f"- {turma.disciplina.nome} (Professores: {professores})")
        altura -= 20
    
    # Adicionar Notas
    p.drawString(100, altura - 20, "Notas:")
    altura -= 40
    notas = Nota.objects.filter(aluno=aluno)
    for nota in notas:
        p.drawString(120, altura, f"- {nota.turma.disciplina.nome}: Avaliação {nota.avaliacao}, Nota: {nota.nota}")
        altura -= 20

    # Adicionar Frequências
    p.drawString(100, altura - 20, "Frequências:")
    altura -= 40
    frequencias = Frequencia.objects.filter(aluno=aluno)
    for frequencia in frequencias:
        status = "Presente" if frequencia.presente else "Ausente"
        p.drawString(120, altura, f"- {frequencia.turma.disciplina.nome}: {frequencia.data} - {status}")
        altura -= 20
    
    # Finaliza o PDF
    p.showPage()
    p.save()
    
    return response
