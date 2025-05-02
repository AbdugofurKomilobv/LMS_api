# urls.py
from django.urls import path
from .views import LessonCreateAPIView, LessonDetailAPIView

app_name = 'lesson'

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson-detail/<int:lesson_id>/<int:group_id>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
   


]
