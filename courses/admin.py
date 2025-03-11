from django.contrib import admin

# Register your models here.
from .models import Person, CategoryCourse, Course, Comment, Response

admin.site.register(Person)
admin.site.register(CategoryCourse)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Response)
