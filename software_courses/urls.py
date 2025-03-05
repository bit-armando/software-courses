from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landingpage.urls')),  # La landingpage será la app principal
    path('courses/', include('courses.urls')),  # Las rutas de courses estarán bajo "/courses/"
]
