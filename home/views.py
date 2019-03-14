from django.shortcuts import render


def index(request):
    # click here to go to hall_pass
    # click her to go to teacher_view
    return render(request, 'home/index.html', {})
