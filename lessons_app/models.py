from common_app.models import BaseModel
from user_app.models import Teacher,Student
from courses_app.models import Group
from django.utils import timezone
from django.db import models

class Lesson(BaseModel):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, related_name="lessons", on_delete=models.CASCADE)
    teacher = models.ForeignKey('user_app.Teacher', related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    lesson_date = models.DateField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.group.title} ({self.lesson_date})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.phone} - {self.lesson.title} - {'Bor' if self.is_present else "Yo'q"}"