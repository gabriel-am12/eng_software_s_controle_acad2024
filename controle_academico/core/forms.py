from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Curso, Disciplina, Turma, Professor, Aluno, Frequencia, Nota


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('nome', 'matricula', 'email', 'telefone')


class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Perfil.USER_TYPES, required=True, label="Eu sou")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Perfil.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
            if profile.user_type == 'student':
                Aluno.objects.create(user=user, profile=profile)
            elif profile.user_type == 'teacher':
                Professor.objects.create(user=user, profile=profile)
        return user

    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'descricao']


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'carga_horaria', 'prerequisitos', 'programa', 'curso']


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['disciplina', 'semestre', 'professores', 'alunos']


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ['data', 'presente']


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['avaliacao', 'nota']


class TeacherAdicionarRemoverEstudantesForm(forms.Form):
    alunos = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.turma = kwargs.pop('turma', None)
        super(TeacherAdicionarRemoverEstudantesForm, self).__init__(*args, **kwargs)
        if self.turma:
            self.fields['alunos'].initial = self.turma.alunos.all()

    def save(self):
        alunos_selecionados = self.cleaned_data['alunos']
        self.turma.alunos.set(alunos_selecionados)
        