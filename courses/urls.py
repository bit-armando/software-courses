from django.urls import path
from . import views

urlpatterns = [
        path('list_courses/', views.list_courses, name='list_courses'),  # Listar cursos
        path('upload/', views.upload_video, name='upload_video'),  # Subir video
]
