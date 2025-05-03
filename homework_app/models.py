from django.db import models
from lessons_app.models import Lesson
from courses_app.models import Group
from user_app.models import Student
from common_app.models import BaseModel


class Homework(models.Model):
    lesson = models.ForeignKey('lessons_app.Lesson', on_delete=models.CASCADE, related_name='homeworks')
    group = models.ForeignKey('courses_app.Group', related_name="homeworks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.lesson}"


class HomeworkAnswer(models.Model):
    homework = models.ForeignKey('homework_app.Homework', on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey('user_app.Student', on_delete=models.CASCADE, related_name='homework_answers')
    answer_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_graded = models.BooleanField(default=False)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.phone} - {self.homework.title}"
