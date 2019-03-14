from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Schedule)
admin.site.register(TimberlaneDaysOff)
admin.site.register(TimberlaneSemester)
admin.site.register(TimberlaneSchedule)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Absence)
