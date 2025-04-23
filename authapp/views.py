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
            messages.success(request, "User registered successfully. Please log in.")
            return redirect('authapp:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authapp/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect('courses:list_courses')
                else:
                    messages.error(request, "Invalid email or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'authapp/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('authapp:login')