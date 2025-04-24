from django.shortcuts import render, redirect, get_object_or_404
from software_courses.storage_backends import MediaStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Course ,Comment ,Response, CategoryCourse
from authapp.models import Person

from .forms import CourseForm
from utils.courses import get_url_without_query

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
def list_courses(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda
    category = request.GET.get('category')  # Obtener la categoría seleccionada

    # Obtener todos los cursos
    courses = Course.objects.all()

    # Filtrar por nombre o descripción
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filtrar por categoría
    if category:
        try:
            category = int(category)
            courses = courses.filter(category__id=category)
        except ValueError:
            pass

    # Paginación: Mostrar 15 cursos por página
    paginator = Paginator(courses, 15)
    page_number = request.GET.get('page')  # Obtener el número de página actual
    page_obj = paginator.get_page(page_number)

    # Obtener todas las categorías para el selector
    categories = CategoryCourse.objects.all()

    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'categories': categories
    })


def course_detail( request ,course_id ):
    course = get_object_or_404(Course, id=course_id)
    person = get_object_or_404(Person, user=request.user)
    
    if course.video:
        video_url = get_url_without_query(str(course.video))
    else:
        video_url = None
    
    if request.method == 'POST' and 'comment' in request.POST:
        comment_text = request.POST.get('comment')
        Comment.objects.create(
            course=course,
            person=person,
            comment=comment_text
        )
    
    if request.method == 'POST' and 'response' in request.POST:
        comment_id = request.POST.get('comment_id')
        response_text = request.POST.get('response')
        comment = get_object_or_404(Comment, id=comment_id)
        Response.objects.create(
            comment=comment,
            person=person,
            response=response_text
        )
    
    comments = course.comments.prefetch_related('responses')
    
    return render( request ,'courses/course_detail.html' ,{
        'course': course,
        'comments': comments,
        'video_url': video_url,
        } )