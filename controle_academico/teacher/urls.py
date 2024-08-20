from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('turmas/<int:turma_id>/registrar_frequencia/', views.RegistrarFrequenciaView.as_view(), name='registrar_frequencia'),
    path('turmas/<int:turma_id>/registrar_nota/', views.RegistrarNotaView.as_view(), name='registrar_nota'),
]