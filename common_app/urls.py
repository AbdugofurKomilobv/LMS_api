from django.urls import path

from common_app.views import LessonAttendanceStatsAPIView,LessonHomeworkStatsAPIView

app_name = 'infos'
urlpatterns = [
       path('stats/lessons/attendance/', LessonAttendanceStatsAPIView.as_view(), name='lesson-attendance-stats'),
       path("statistika/stats/lessons/homeworks/", LessonHomeworkStatsAPIView.as_view()),
]

