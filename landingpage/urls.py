from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.home, name='home'),  # Ruta principal de la landingpage
]
