from django.urls import path
from django.shortcuts import redirect
from . import views, views_aluno, views_professor, views_administrador

urlpatterns = [
    # Login e Registro
    path('', views.redirect_user_based_on_type),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------------------- Estudante ----------------------------------

    path('aluno/', views_aluno.home_view, name='aluno_inicio'),
    path('aluno/turma/<int:turma_id>/', views_aluno.turma_view, name='aluno_turma_details'),
    path('aluno/turma/<int:turma_id>/boletim/', views_aluno.boletim_view, name='aluno_turma_boletim'),
    
    # ---------------------------- Professor ----------------------------------

    path('professor/', views_professor.home_view, name='professor_inicio'),
    path('professor/turma/<int:turma_id>/', views_professor.turma_details_view, name='professor_turma_details'),

    # ---------------------------- Administrador ------------------------------

    path('administrador/', views_administrador.home_view, name='administrador_inicio'),

    # Aluno
    path('administrador/alunos/', views_administrador.aluno_list_view, name='administrador_aluno_list'),
    path('administrador/alunos/create', views_administrador.aluno_create_view, name='administrador_aluno_create'),
    path('administrador/alunos/<int:pk>', views_administrador.aluno_details_view, name='administrador_aluno_details'),
    path('administrador/alunos/<int:pk>/edit', views_administrador.aluno_update_view, name='administrador_aluno_update'),
    path('administrador/alunos/<int:pk>/delete', views_administrador.aluno_delete_view, name='administrador_aluno_delete'),

    # Turma
    path('administrador/turmas/', views_administrador.turma_list_view, name='administrador_turma_list'),
    path('administrador/turmas/create', views_administrador.turma_create_view, name='administrador_turma_create'),
    path('administrador/turmas/<int:pk>', views_administrador.turma_details_view, name='administrador_turma_details'),
    path('administrador/turmas/<int:pk>/edit', views_administrador.turma_update_view, name='administrador_turma_update'),
    path('administrador/turmas/<int:pk>/delete', views_administrador.turma_delete_view, name='administrador_turma_delete'),

    # Disciplina
    path('administrador/disciplinas/', views_administrador.disciplina_list_view, name='administrador_disciplina_list'),
    path('administrador/disciplinas/create', views_administrador.create_disciplina_view, name='administrador_disciplina_create'),
    path('administrador/disciplinas/<int:pk>', views_administrador.disciplina_details_view, name='administrador_disciplina_details'),
    path('administrador/disciplinas/<int:pk>/edit', views_administrador.edit_disciplina_view, name='administrador_disciplina_update'),
    path('administrador/disciplinas/<int:pk>/delete', views_administrador.delete_disciplina_view, name='administrador_disciplina_delete'),

    # Curso
    path('administrador/cursos/', views_administrador.curso_list_view, name='administrador_curso_list'),
    path('administrador/cursos/create', views_administrador.create_curso_view, name='administrador_curso_create'),
    path('administrador/cursos/<int:pk>', views_administrador.curso_details_view, name='administrador_curso_details'),
    path('administrador/cursos/<int:pk>/edit', views_administrador.edit_curso_view, name='administrador_curso_update'),
    path('administrador/cursos/<int:pk>/delete', views_administrador.delete_curso_view, name='administrador_curso_delete'),

]
