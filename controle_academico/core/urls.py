from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Login e Registro
    path('', lambda request: redirect('login')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # Estudante, Professor e Administrador
    path('student/', include('students.urls')),
    path('teacher/', include('teacher.urls')),

    path('administrator/', views.administrator_dashboard, name='administrator_dashboard'),
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
]
