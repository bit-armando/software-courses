import boto3
import re
from django.conf import settings

def get_presigned_url(file_key):
    prefix = 'media/videos/'
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_STORAGE_BUCKET_NAME
    )
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_key
        },
        ExpiresIn=3600  # Tiempo de expiración en segundos (1 hora)
    )
    return url


def get_url_without_query(url):
    match = re.match(r"([^?]+)", url)
    if match:
        return match.group(1)  # Retorna la parte antes del '?'
    return url  # Si no hay '?', retorna la URL completa