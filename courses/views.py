from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def course_list(request):
    return render(request, 'courses/course_list.html')

# def course_detail(request, course_id):
#     return render(request, 'courses/course_detail.html', {'course_id': course_id})


def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        file_name = default_storage.save(video.name, ContentFile(video.read()))
        file_url = default_storage.url(file_name)
        print("Archivo guardado en:", file_url)
        return render(request, 'courses/course_list.html', {'file_url': file_url})
    return render(request, 'courses/upload_video.html')

