from django.urls import path
from . import views

urlpatterns = [
        path( '' ,views.course_list ,name='course_list' ) ,  # Página principal de cursos
        # path('<int:course_id>/', views.course_detail, name='course_detail'),  # Detalle del curso
        path('list_courses/', views.list_courses, name='list_courses'),  # Listar cursos
        path('upload/', views.upload_video, name='upload_video'),  # Subir video
]
