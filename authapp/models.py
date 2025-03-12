from django.db import models
from django.contrib.auth.models import User

from software_courses.storage_backends import MediaStorage


class Person(models.Model):
    user = models.OneToOneField( User ,on_delete=models.CASCADE )
    degrade = models.CharField(verbose_name='Degrade', max_length=255 ,blank=True ,null=True)
    instructor = models.BooleanField( verbose_name='Is Instructor', default=False )
    image = models.ImageField( upload_to="person_img/" ,storage=MediaStorage() ,blank=True ,null=True )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'