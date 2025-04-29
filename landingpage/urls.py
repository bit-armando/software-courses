from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.home, name='home'),  # Ruta principal de la landingpage
    path('terms/', views.terms, name='terms'),  # Ruta para los términos y condiciones
    path('privacy/', views.privacy, name='privacy'),  # Ruta para la política de privacidad
]
