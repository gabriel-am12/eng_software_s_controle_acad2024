from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('turma/<int:id>', views.class_details, name='student_class_details'),
]