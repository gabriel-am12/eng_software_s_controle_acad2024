from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpRequest

from .models import Perfil

def user_type_required(user_type, redirect_url='/'):
    def decorator(func):
        @login_required(login_url='/login')
        def wrapper(request: HttpRequest, *args, **kwargs):
            user = request.user
            perfil = Perfil.objects.filter(user=user).first()
            print("Passou por aqui!")

            if perfil is None or perfil.user_type != user_type:
                return redirect(redirect_url)

            return func(request, *args, **kwargs)
        return wrapper

    return decorator

student_required = user_type_required('student')
teacher_required = user_type_required('teacher')
admin_required = user_type_required('administrator')
