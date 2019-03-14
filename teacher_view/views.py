from django.shortcuts import render

def index(request):
    return render(request, 'teacher_view/index.html', {})
