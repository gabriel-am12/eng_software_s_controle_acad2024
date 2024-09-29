from datetime import datetime, time
from django.contrib.auth.models import User
from django.db.models import (
    Model, 
    ForeignKey, 
    ManyToManyField, 
    OneToOneField, 
    CharField,
    IntegerField,
    EmailField,
    TextField,
    BooleanField,
    DateField,
    DecimalField,
    FileField,
    CASCADE,
)

class Perfil(Model):
    USER_TYPES = (
        ('student', 'Estudante'),
        ('teacher', 'Professor'),
        ('administrator', 'Administrador'),
    )
    user = OneToOneField(User, on_delete=CASCADE)
    user_type = CharField(max_length=15, choices=USER_TYPES)

    def __str__(self):
        return self.user.username


class Professor(Model):
    user = OneToOneField(User, on_delete=CASCADE, null = True, blank=True)
    profile = OneToOneField(Perfil, on_delete=CASCADE, null = True, blank=True)
    nome = CharField(max_length=100)
    email = EmailField()

    def __str__(self):
        return self.nome


class Aluno(Model):
    user = OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    profile = OneToOneField(Perfil, on_delete=CASCADE, null=True, blank=True)
    nome = CharField(max_length=100)
    matricula = CharField(max_length=15)
    telefone = CharField(max_length=12, blank=True, null=True)
    email = EmailField()

    def __str__(self):
        return self.nome


class Curso(Model):
    nome = CharField(max_length=100)
    descricao = TextField()

    def __str__(self):
        return self.nome
    

class Disciplina(Model):
    nome = CharField(max_length=100)
    carga_horaria = IntegerField()
    prerequisitos = ManyToManyField('self', blank=True, symmetrical=False)
    programa = TextField()
    curso = ForeignKey(Curso, on_delete=CASCADE, related_name='disciplinas', blank=True, null=True) # Revisar essa relação

    def __str__(self):
        return self.nome


class Turma(Model):
    disciplina = ForeignKey(Disciplina, on_delete=CASCADE, related_name='turmas')
    semestre = CharField(max_length=6)  # Ex: "2024-1"
    professores = ManyToManyField('Professor', related_name='turmas', blank=True)
    alunos = ManyToManyField('Aluno', related_name='turmas_set', blank=True)

    def __str__(self):
        return f'{self.disciplina.nome} - {self.semestre}'
 

class Frequencia(Model):
    aluno = ForeignKey(Aluno, on_delete=CASCADE)
    turma = ForeignKey(Turma, on_delete=CASCADE)
    data = DateField()
    presente = BooleanField(default=False)

    def __str__(self):
        return f'{self.aluno} - {self.turma} - {self.data}'


class Nota(Model):
    aluno = ForeignKey(Aluno, on_delete=CASCADE)
    turma = ForeignKey(Turma, on_delete=CASCADE)
    avaliacao = IntegerField(choices=[(1, 'Avaliação 1'), (2, 'Avaliação 2'), (3, 'Avaliação 3'), (4, 'Avaliação 4')])
    nota = DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.aluno} - {self.turma} - Avaliação {self.avaliacao}: {self.nota}'


class Noticia(Model):
    turma = ForeignKey(Turma, on_delete=CASCADE, related_name="noticias")
    titulo = CharField(verbose_name="título", max_length=120)
    conteudo = TextField(verbose_name="conteúdo")
    data = DateField()


class Atividade(Model):
    turma = ForeignKey(Turma, on_delete=CASCADE, related_name="atividades")
    titulo = CharField(verbose_name="título", max_length=120)
    conteudo = TextField(verbose_name="conteúdo")
    arquivos = FileField(blank=True, null=True)
    data_limite = DateField(default=datetime.now)
