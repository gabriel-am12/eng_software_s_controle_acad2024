from django.contrib import admin
from .models import Curso, Disciplina, Turma, Aluno, Professor

admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Professor)
