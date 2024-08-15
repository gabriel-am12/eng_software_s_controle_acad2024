from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Estudante'),
        ('teacher', 'Professor'),
        ('administrator', 'Administrador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=15, choices=USER_TYPES)

    def __str__(self):
        return self.user.username

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome
        
    
class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    prerequisitos = models.ManyToManyField('self', blank=True, symmetrical=False)
    programa = models.TextField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='disciplinas')

    def __str__(self):
        return self.nome

class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='turmas')
    semestre = models.CharField(max_length=6)  # Ex: "2024-1"
    professores = models.ManyToManyField('Professor', related_name='turmas')
    alunos = models.ManyToManyField('Aluno', related_name='turmas')

    def __str__(self):
        return f'{self.disciplina.nome} - {self.semestre}'
