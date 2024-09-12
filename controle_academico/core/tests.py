from django.test import TestCase
from django.contrib.auth.models import User
from .models import Perfil, Professor, Aluno, Curso, Disciplina, Turma, Frequencia, Nota
from datetime import date


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


class ModelsTestCase(TestCase):
    
    def setUp(self):
        # Setup básico de um usuário para associar aos perfis
        self.user_student = User.objects.create_user(username='student_user', password='student_pass')
        self.user_teacher = User.objects.create_user(username='teacher_user', password='teacher_pass')
        
        # Criação do perfil do aluno e do professor
        self.profile_student = Perfil.objects.create(user=self.user_student, user_type='student')
        self.profile_teacher = Perfil.objects.create(user=self.user_teacher, user_type='teacher')
        
        # Criação do professor
        self.professor = Professor.objects.create(user=self.user_teacher, profile=self.profile_teacher, nome='Professor X', email='professor@example.com')
        
        # Criação do aluno
        self.aluno = Aluno.objects.create(user=self.user_student, profile=self.profile_student, nome='Aluno Y', matricula='20230001', telefone='123456789', email='aluno@example.com')
        
        # Criação do curso e da disciplina
        self.curso = Curso.objects.create(nome='Engenharia', descricao='Curso de Engenharia')
        self.disciplina = Disciplina.objects.create(nome='Matemática', carga_horaria=60, programa='Álgebra e Cálculo', curso=self.curso)
        
        # Criação da turma
        self.turma = Turma.objects.create(disciplina=self.disciplina, semestre='2024-1')
        self.turma.professores.add(self.professor)
        self.turma.alunos.add(self.aluno)

    def test_perfil_str(self):
        """Testa o método __str__ da classe Perfil"""
        self.assertEqual(str(self.profile_student), 'student_user')
        self.assertEqual(str(self.profile_teacher), 'teacher_user')
        
    def test_professor_str(self):
        """Testa o método __str__ da classe Professor"""
        self.assertEqual(str(self.professor), 'Professor X')
        
    def test_aluno_str(self):
        """Testa o método __str__ da classe Aluno"""
        self.assertEqual(str(self.aluno), 'Aluno Y')

    def test_curso_str(self):
        """Testa o método __str__ da classe Curso"""
        self.assertEqual(str(self.curso), 'Engenharia')

    def test_disciplina_str(self):
        """Testa o método __str__ da classe Disciplina"""
        self.assertEqual(str(self.disciplina), 'Matemática')

    def test_turma_str(self):
        """Testa o método __str__ da classe Turma"""
        self.assertEqual(str(self.turma), 'Matemática - 2024-1')

    def test_frequencia_str(self):
        """Testa o método __str__ da classe Frequencia"""
        frequencia = Frequencia.objects.create(aluno=self.aluno, turma=self.turma, data=date.today(), presente=True)
        self.assertEqual(str(frequencia), f'Aluno Y - Matemática - 2024-1 - {date.today()}')
        
    def test_nota_str(self):
        """Testa o método __str__ da classe Nota"""
        nota = Nota.objects.create(aluno=self.aluno, turma=self.turma, avaliacao=1, nota=9.5)
        self.assertEqual(str(nota), 'Aluno Y - Matemática - 2024-1 - Avaliação 1: 9.5')

    def test_turma_has_professor(self):
        """Testa se a turma tem um professor associado"""
        self.assertIn(self.professor, self.turma.professores.all())

    def test_turma_has_aluno(self):
        """Testa se a turma tem um aluno associado"""
        self.assertIn(self.aluno, self.turma.alunos.all())

    def test_disciplina_curso_relation(self):
        """Testa a relação entre Disciplina e Curso"""
        self.assertEqual(self.disciplina.curso, self.curso)
        
    def test_frequencia_creation(self):
        """Testa a criação de uma instância de Frequencia"""
        frequencia = Frequencia.objects.create(aluno=self.aluno, turma=self.turma, data=date.today(), presente=False)
        self.assertFalse(frequencia.presente)
        
    def test_nota_creation(self):
        """Testa a criação de uma instância de Nota"""
        nota = Nota.objects.create(aluno=self.aluno, turma=self.turma, avaliacao=2, nota=7.0)
        self.assertEqual(nota.nota, 7.0)

