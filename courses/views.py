from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from software_courses.storage_backends import MediaStorage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Course,Comment,Response,CategoryCourse,Material
from authapp.models import Person

from .forms import CourseForm, MaterialForm
from utils.courses import get_url_without_query

@login_required(login_url='/auth/login/')
def upload_video(request):
    if not request.user.is_superuser:
        return redirect('courses:list_courses')  # Redirigir si no es superusuario

    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)

        if course_form.is_valid():
            # Guardar el curso
            course = course_form.save(commit=False)
            # course.person = Person.objects.get(user=request.user)  # Relacionar con el usuario actual
            course.save()

            # Procesar múltiples archivos subidos
            files = request.FILES.getlist('file')  # Obtener todos los archivos subidos
            for file in files:
                Material.objects.create(course=course, file=file, title=file.name)

            return redirect('courses:list_courses')  # Redirigir a la lista de cursos
    else:
        course_form = CourseForm()

    return render(request, 'courses/upload_video.html', {
        'course_form': course_form,
    })


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


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    person = get_object_or_404(Person, user=request.user)

    # Obtener la URL del video sin parámetros de consulta
    if course.video:
        video_url = get_url_without_query(str(course.video))
    else:
        video_url = None

    # Manejar la creación de comentarios
    if request.method == 'POST' and 'comment' in request.POST:
        comment_text = request.POST.get('comment')
        Comment.objects.create(
            course=course,
            person=person,
            comment=comment_text
        )

    # Manejar la creación de respuestas
    if request.method == 'POST' and 'response' in request.POST:
        comment_id = request.POST.get('comment_id')
        response_text = request.POST.get('response')
        comment = get_object_or_404(Comment, id=comment_id)
        Response.objects.create(
            comment=comment,
            person=person,
            response=response_text
        )

    # Obtener los comentarios y materiales relacionados
    comments = course.comments.prefetch_related('responses')
    materials = course.materials.all()  # Acceder a los materiales relacionados

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'comments': comments,
        'materials': materials,
        'video_url': video_url,
    })