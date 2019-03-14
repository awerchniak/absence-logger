from django.urls import path

from . import views

app_name = 'teacher_view'
urlpatterns = [
    path('', views.index, name='index'),
]
