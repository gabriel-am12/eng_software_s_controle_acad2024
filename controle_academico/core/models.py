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