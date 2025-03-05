from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),  # Página principal de cursos
    # path('<int:course_id>/', views.course_detail, name='course_detail'),  # Detalle del curso
]
