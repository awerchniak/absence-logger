from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Absence, Course, Student

def sign_out_page(request, course_id):
    """Render a sign out page for a given course.

    This page displays a drop down of all of the students in the given course. Students may select
    their name from the dropdown and sign out (or sign back in if they're already signed out).

    """
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'hall_pass/sign_out_page.html', {'course': course})

def sign_out_action(request, course_id):
    """Sign a student out of or back into class.

    If the student is not signed out, create a new Absence for them. If they are signed out, sign
    them back in by completing their current_absence.

    """
    course = get_object_or_404(Course, id=course_id)
    try:
        student = Student.objects.get(id=request.POST['student'])
    except (KeyError, Student.DoesNotExist):
        return render(request, 'hall_pass/sign_out_page.html', {
            'course': course,
            'error_message': str(request.POST),
        })
    else:
        if student.current_absence is None:
            # create a new absence
            absence = Absence(
                student=student,
                course=course,
                time_out=datetime.now(),
                reason=request.POST['reason']
            )
            absence.save()

            student.current_absence = absence
            student.save()
        else:
            # complete current absence
            absence = student.current_absence
            absence.time_in = datetime.now()
            absence.save()

            student.current_absence = None
            student.save()
        return HttpResponseRedirect(
            reverse('hall_pass:sign_out_result', args=(course_id, student.id))
        )

def sign_out_result(request, course_id, student_id):
    # TODO: use django.views.generic.DetailView
    return render(request, 'hall_pass/sign_out_result.html', {
        'course_id': course_id,
    })

def index(request):
    """Render an index, which links to course pages.

    This page simply retrieves all courses from the database and links to their appropriate sign
    out pages.

    """
    # TODO: Use django.views.generic.ListView
    courses = Course.objects.order_by('-name')
    context = {
        'courses': courses,
    }
    return render(request, 'hall_pass/index.html', context)
