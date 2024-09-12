from django.test import TestCase
from .models import Turma, Disciplina, Professor, Aluno


class TurmaModelTest(TestCase):
    def setUp(self):
        """Cria instâncias necessárias para os testes"""

        self.disciplina = Disciplina.objects.create(
            nome='Matemática',
            carga_horaria=60,
            programa='Disciplina que estuda matemática',
        )

        self.professor1 = Professor.objects.create(nome='Professor A', email="professor.a@email.com")
        self.professor2 = Professor.objects.create(nome='Professor B', email="professor.b@email.com")

        self.aluno1 = Aluno.objects.create(nome='Aluno 1', matricula="0001", email="aluno1@email.com")
        self.aluno2 = Aluno.objects.create(nome='Aluno 2', matricula="0002", email="aluno2@email.com")
    
    def test_create_turma(self):
        """Testa a criação de uma instância de Turma com os campos obrigatórios"""

        turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        turma.save()

        self.assertEqual(turma.semestre, '2024-1')
        self.assertEqual(turma.disciplina.nome, 'Matemática')
    
    def test_add_professores_to_turma(self):
        """Testa a adição de professores na Turma (ManyToManyField)"""

        turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        turma.professores.add(self.professor1, self.professor2)
        turma.save()

        self.assertEqual(turma.professores.count(), 2)
        self.assertIn(self.professor1, turma.professores.all())
        self.assertIn(self.professor2, turma.professores.all())

    def test_add_alunos_to_turma(self):
        """Testa a adição de alunos na Turma (ManyToManyField)"""

        turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        turma.alunos.add(self.aluno1, self.aluno2)
        turma.save()

        self.assertEqual(turma.alunos.count(), 2)
        self.assertIn(self.aluno1, turma.alunos.all())
        self.assertIn(self.aluno2, turma.alunos.all())

    def test_str_representation(self):
        """Testa a representação da string do modelo Turma"""

        turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        turma.save()

        self.assertEqual(str(turma), 'Matemática - 2024-1')

    def test_delete_disciplina_cascade(self):
        """Testa se a remoção de uma Disciplina remove as Turmas associadas (CASCADE)"""

        turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        turma.save()

        self.disciplina.delete()
        with self.assertRaises(Turma.DoesNotExist):
            Turma.objects.get(id=turma.id)
