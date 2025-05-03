from django.db import models
from django.contrib.auth.models import User

from software_courses.storage_backends import MediaStorage
from authapp.models import Person


class CategoryCourse(models.Model):
    name = models.CharField(verbose_name='Category Name', max_length=255, default='Programación', unique=True)
    created_at = models.DateTimeField(verbose_name='Created', auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(verbose_name='Title',max_length=255)
    category = models.ForeignKey(CategoryCourse, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='courses_img/', storage=MediaStorage(), blank=True, null=True)
    short_description = models.TextField(verbose_name='Short Description', blank=True, null=True)
    description = models.TextField(verbose_name='Largue Description',blank=True, null=True)
    video = models.FileField(upload_to='videos/', storage=MediaStorage(), blank=True, null=True)
    # person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.person.user.first_name} {self.person.user.last_name} - {self.course.title}'


class Response(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='responses')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    response = models.TextField(verbose_name='Response', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.person.user.first_name} {self.person.user.last_name} - {self.comment.course.title}'


class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(verbose_name='Title', max_length=255)
    file = models.FileField(upload_to='materials/', storage=MediaStorage(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.course.title}'