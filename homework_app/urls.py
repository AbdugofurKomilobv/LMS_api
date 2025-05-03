from django.urls import path
from homework_app.views import HomeworkCreateAPIView,HomeworkAnswerListAPIView,HomeworkAnswerGradeAPIView

urlpatterns = [
    # Teacher
    path('homework/create/', HomeworkCreateAPIView.as_view(), name='homework-create'),
    path('teacher/homework/<int:homework_id>/answers/', HomeworkAnswerListAPIView.as_view(), name='homework-answers'),
    path('teacher/homework/answer/<int:homework_answer_id>/grade/', HomeworkAnswerGradeAPIView.as_view(), name='teacher-homework-grade'),




]
