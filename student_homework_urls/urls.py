from django.urls import path
from homework_app.views import StudentHomeworkListAPIView,StudentHomeworkAnswerAPIView,StudentBaxosikAnswerAPIView,StudentGradedHomeworkAPIView

urlpatterns = [
    # o'quvchi
    path('student/homeworks/', StudentHomeworkListAPIView.as_view(), name='student-homework-list'),
path('student/homework/<int:homework_id>/answer/', StudentHomeworkAnswerAPIView.as_view(), name='student-homework-answer'),
path('student/baxo/<int:homework_id>/answer/', StudentBaxosikAnswerAPIView.as_view(), name='student-homework-answer'),
 path('student/graded-homeworks/', StudentGradedHomeworkAPIView.as_view(), name='student-graded-homeworks'),





]
