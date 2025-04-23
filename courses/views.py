from django.shortcuts import render, redirect
from software_courses.storage_backends import MediaStorage
from django.contrib.auth.decorators import login_required

from .models import Course ,Comment ,Response
from authapp.models import Person

from .forms import CourseForm


# def course_detail(request, course_id):
#     return render(request, 'courses/course_detail.html', {'course_id': course_id})


@login_required(login_url='/auth/login/')
def upload_video(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el curso y subir el video a S3
            course = form.save(commit=False)
            if 'video' in request.FILES:
                video = request.FILES['video']
                media_storage = MediaStorage()
                video_name = media_storage.save(f"videos/{video.name}", video)
                course.video = media_storage.url(video_name)
            course.save()
            return redirect('courses:list_courses')  # Redirigir a la lista de cursos
    else:
        form = CourseForm()

    return render(request, 'courses/upload_video.html', {'form': form})


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


@login_required(login_url='/auth/login/')
def list_courses( request ):
    courses = Course.objects.all()
    return render( request ,'courses/course_list.html' ,{'courses': courses} )


def course_detail( request ,course_id ):
    course = Course.objects.get( id=course_id )
    return render( request ,'courses/course_detail.html' ,{'course': course} )