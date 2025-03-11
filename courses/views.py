from django.shortcuts import render
from software_courses.storage_backends import MediaStorage

from .models import Course

def course_list(request):
    return render(request, 'courses/course_list.html')

# def course_detail(request, course_id):
#     return render(request, 'courses/course_detail.html', {'course_id': course_id})


def upload_video( request ):
    if request.method == 'POST' and request.FILES.get( 'video' ):
        title = request.POST.get('title')
        video = request.FILES['video']
        image = request.FILES['image']
        short_description = request.POST['short_description']
        description = request.POST['description']

        # Instanciar el almacenamiento S3
        media_storage = MediaStorage()

        # Guardar el archivo en S3
        video_name = media_storage.save( f"videos/{video.name}" ,video )
        video_url = media_storage.url( video_name )

        image_name = media_storage.save( f"courses_img/{image.name}" ,image )
        image_url = media_storage.url( image_name )

        # Guardar la URL del video en el modelo Course
        Course.objects.create(
                title=title,
                image= image_url,  # Puedes asignar una imagen aquí
                short_description=short_description,
                description=description,
                video=video_url
        )

    return render( request ,'courses/upload_video.html' )