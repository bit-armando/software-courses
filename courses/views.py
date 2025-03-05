from django.shortcuts import render

from django.shortcuts import render

def course_list(request):
    return render(request, 'courses/course_list.html')

# def course_detail(request, course_id):
#     return render(request, 'courses/course_detail.html', {'course_id': course_id})

