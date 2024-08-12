from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Profile

def redirect_user_based_on_type(user):
    if user.profile.user_type == 'student':
        return redirect('student_dashboard')
    elif user.profile.user_type == 'teacher':
        return redirect('teacher_dashboard')
    elif user.profile.user_type == 'administrator':
        return redirect('administrator_dashboard')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_based_on_type(user)
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user_based_on_type(user)
        else:
            return render(request, 'login.html', {'error': 'Username ou senha inválidos'})
    return render(request, 'login.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def administrator_dashboard(request):
    return render(request, 'administrator_dashboard.html')
