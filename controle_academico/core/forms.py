from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Curso, Disciplina, Turma, Professor, Aluno, Frequencia, Nota

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPES, required=True, label="Eu sou")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(
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
       