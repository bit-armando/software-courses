from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
            label="Contraseña",
            widget=forms.PasswordInput(attrs={
                'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Contraseña'
            })
        )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirmar Contraseña'
            })
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'Primer Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Primer Nombre'
            }),
            'last_name': forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Apellido'
            }),
        }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid email or password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data