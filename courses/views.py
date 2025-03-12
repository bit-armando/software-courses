from django.shortcuts import render
from software_courses.storage_backends import MediaStorage

from .models import Course ,Comment ,Response
from authapp.models import Person


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


def course_comment( request ):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        person_id = request.POST.get('person_id')
        comment = request.POST.get('comment')

        course = Course.objects.get( id=course_id )
        person = Person.objects.get( id=person_id )

        Comment.objects.create(
            course=course,
            person=person,
            comment=comment
        )

    return render( request ,'courses/course.html' )


def response_comment( request ):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        person_id = request.POST.get('person_id')
        response = request.POST.get('response')

        comment = Comment.objects.get( id=comment_id )
        person = Person.objects.get( id=person_id )

        Response.objects.create(
            comment=comment,
            person=person,
            response=response
        )

    return render( request ,'courses/course.html' )


def list_courses( request ):
    courses = Course.objects.all()
    return render( request ,'courses/list_courses.html' ,{'courses': courses} )


def course_detail( request ,course_id ):
    course = Course.objects.get( id=course_id )
    return render( request ,'courses/course_detail.html' ,{'course': course} )