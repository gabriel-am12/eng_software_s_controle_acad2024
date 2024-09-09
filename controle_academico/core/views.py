from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpRequest

from .models import Turma, Aluno, Frequencia, Nota
from .forms import SignUpForm

# Redirect, Registro e Login
@login_required(login_url='/login')
def redirect_user_based_on_type(request: HttpRequest):
    user = request.user
    if user.perfil.user_type == 'student':
        return redirect('aluno_inicio')
    elif user.perfil.user_type == 'teacher':
        return redirect('professor_inicio')
    elif user.perfil.user_type == 'administrator':
        return redirect('administrador_inicio')

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
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Username ou senha inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

# Relatórios / Boletins
class RelatorioAlunoView(View):
    def get(self, request, aluno_id):
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        turmas = Turma.objects.filter(alunos=aluno).select_related('disciplina__curso')
        notas = Nota.objects.filter(aluno=aluno)
        frequencias = Frequencia.objects.filter(aluno=aluno)
        
        previous_url = request.META.get('HTTP_REFERER', '/professor_inicio')

        context = {
            'aluno': aluno,
            'turmas': turmas,
            'notas': notas,
            'frequencias': frequencias,
            'redirect_url': previous_url,
        }

        return render(request,'relatorio_aluno.html', context)
