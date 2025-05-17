from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm
from authapp.models import Person

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Crear un perfil para el usuario
            Person.objects.create(user=user)
            messages.success(request, "Usuario registrado con éxito, por favor inicia sesión.")
            return redirect('authapp:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authapp/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.success(request, "¡Bienvenido! Has iniciado sesión correctamente.")
                    return redirect('courses:list_courses')
                else:
                    form.add_error(None, "Correo electrónico o contraseña incorrectos")
            except User.DoesNotExist:
                form.add_error(None, "Correo electrónico o contraseña incorrectos")
    else:
        form = UserLoginForm()
    return render(request, 'authapp/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente!.")
    return redirect('authapp:login')