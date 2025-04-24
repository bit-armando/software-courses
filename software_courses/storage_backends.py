from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = "public-read"  # Para archivos estáticos públicos
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    # default_acl = "public-read"  # Los archivos multimedia suelen ser privados
    file_overwrite = False