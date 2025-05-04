from django.urls import path

from common_app.views import LessonAttendanceStatsAPIView,LessonHomeworkStatsAPIView,TeacherCourseView

app_name = 'infos'
urlpatterns = [
       path('stats/lessons/attendance/', LessonAttendanceStatsAPIView.as_view(), name='lesson-attendance-stats'),
       path("statistika/stats/lessons/homeworks/", LessonHomeworkStatsAPIView.as_view()),
       path('teacher/course/<int:pk>/',TeacherCourseView.as_view(),name='teacher_course')

           
]

