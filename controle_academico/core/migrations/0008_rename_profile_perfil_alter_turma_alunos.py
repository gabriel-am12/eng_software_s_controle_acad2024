# Generated by Django 5.1 on 2024-08-31 02:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_aluno_turmas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Perfil',
        ),
        migrations.AlterField(
            model_name='turma',
            name='alunos',
            field=models.ManyToManyField(blank=True, related_name='turmas_set', to='core.aluno'),
        ),
    ]
