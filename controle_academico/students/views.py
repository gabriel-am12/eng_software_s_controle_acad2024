from re import template
from django.shortcuts import render, get_object_or_404
from core.models import Aluno, Turma, Nota

# Create your views here.
# Estudante, Professor e Administrador
def student_dashboard(request):
    return render(request, 'students/student_dashboard.html')

def class_details(request, id: int):
    user = request.user
    
    aluno = get_object_or_404(Aluno.objects, user=user)
    turma = get_object_or_404(Turma.objects, id=id)
    notas = Nota.objects.filter(aluno=aluno, turma=turma).all()

    return render(
        request=request,
        template_name="students/class_details.html",
        context={
            'turma': turma,
            'frequencia': '80%',
            'notas': notas
        }
    )