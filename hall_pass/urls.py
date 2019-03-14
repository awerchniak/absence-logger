from django.urls import path

from . import views

app_name = 'hall_pass'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>/', views.sign_out_page, name='sign_out_page'),
    path('<int:course_id>/sign_out/', views.sign_out_action, name='sign_out_action'),
    path('<int:course_id>/<int:student_id>/result/', views.sign_out_result, name='sign_out_result')
]
