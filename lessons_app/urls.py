from django.urls import path
from . import views

app_name = 'lessons_app'

urlpatterns = [
    path('create-lesson/', views.CreateLessonView.as_view(), name='create_lesson'),
    path('attendance/<int:lesson_id>/', views.AttendanceListView.as_view(), name='attendance_list'),
    path("attendance-yo'qlama/<int:lesson_id>/update/", views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('lessons/group-lessons/<int:group_id>/', views.LessonListView.as_view(), name='lesson_list'),
]
