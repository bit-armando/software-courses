from django.urls import path
from . import views


app_name = "courses"

urlpatterns = [
        path('list_courses/', views.list_courses, name='list_courses'),  # Listar cursos
        path('upload/', views.upload_video, name='upload_video'),
        path('detail/<int:course_id>/', views.course_detail, name='course_detail'),  # Detalle del curso
        path('history/', views.course_history, name='course_history'),  # Historial de cursos
]
