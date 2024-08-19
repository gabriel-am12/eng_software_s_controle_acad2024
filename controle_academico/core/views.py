from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from .models import Profile, Curso, Disciplina, Turma, Aluno, Professor, Frequencia, Nota
from .forms import SignUpForm, CursoForm, DisciplinaForm, TurmaForm, FrequenciaForm, NotaForm

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
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

class TeacherDashboardView(View):
    def get(self, request):
        professor = request.user.professor  
        turmas = Turma.objects.filter(professores=professor)
        context = {'turmas': turmas}
        return render(request, 'teacher_dashboard.html', context)

def administrator_dashboard(request):
    return render(request, 'administrator_dashboard.html')

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
        context['alunos'] = Aluno.objects.all()  # Certifique-se de que este queryset retorna os alunos registrados corretamente
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

# Frequência e Nota

class RegistrarFrequenciaView(View):
    def get(self, request, turma_id):
        turma = Turma.objects.get(id=turma_id)
        alunos = turma.alunos.all()
        form = FrequenciaForm()
        context = {'turma': turma, 'alunos': alunos, 'form': form}
        return render(request, 'registrar_frequencia.html', context)

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
        return render(request, 'registrar_frequencia.html', {'turma': turma, 'alunos': turma.alunos.all(), 'form': form})

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
