from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Login e Registro
    path('', lambda request: redirect('login')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # Estudante, Professor e Administrador
    path('student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('administrator/', views.AdministratorDashboardView.as_view(), name='administrator_dashboard'),
    # Curso
    path('cursos/', views.CursoListView.as_view(), name='curso_list'),
    path('cursos/<int:pk>/', views.CursoDetailView.as_view(), name='curso_detail'),
    #path('cursos/create/', views.CursoCreateView.as_view(), name='curso_create'),
    #path('cursos/<int:pk>/update/', views.CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<int:pk>/delete/', views.CursoDeleteView.as_view(), name='curso_delete'),
    # Disciplina
    path('disciplinas/', views.DisciplinaListView.as_view(), name='disciplina_list'),
    path('disciplinas/<int:pk>/', views.DisciplinaDetailView.as_view(), name='disciplina_detail'),
    #path('disciplinas/create/', views.DisciplinaCreateView.as_view(), name='disciplina_create'),
    #path('disciplinas/<int:pk>/update/', views.DisciplinaUpdateView.as_view(), name='disciplina_update'),
    path('disciplinas/<int:pk>/delete/', views.DisciplinaDeleteView.as_view(), name='disciplina_delete'),
    # Turmas
    path('turmas/', views.TurmaListView.as_view(), name='turma_list'),
    path('turmas/<int:pk>/', views.TurmaDetailView.as_view(), name='turma_detail'),
    #path('turmas/create/', views.TurmaCreateView.as_view(), name='turma_create'),
    #path('turmas/<int:pk>/update/', views.TurmaUpdateView.as_view(), name='turma_update'),
    path('turmas/<int:pk>/delete/', views.TurmaDeleteView.as_view(), name='turma_delete'),
    path('turmas/<int:turma_id>/registrar_frequencia/', views.RegistrarFrequenciaView.as_view(), name='registrar_frequencia'),
    path('turmas/<int:turma_id>/registrar_nota/', views.RegistrarNotaView.as_view(), name='registrar_nota'),
    path('turmas/<int:turma_id>/gerenciar_estudantes/', views.TeacherAdicionarRemoverEstudantesView.as_view(), name='gerenciar_estudantes'),
    path('relatorio_aluno/<int:aluno_id>/', views.RelatorioAlunoView.as_view(), name='relatorio_aluno'),
]
