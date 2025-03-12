from django.contrib.auth.models import User
from django.shortcuts import render

from authapp.models import Person


def register_user(request):
    return render(request, 'authapp/register.html')


def login_user(request):
    return render(request, 'authapp/login.html')


def logout_user(request):
    return render(request, 'authapp/logout.html')


def new_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Crear un usuario
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Crear un perfil
        Person.objects.create(
            user=user
        )
    return render(request, 'authapp/login.html')