from django.db import models
from common_app.models import BaseModel
from django.utils import timezone
from user_app.models import Student,Teacher
from courses_app.models import Group

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.group.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('kelgan', 'Kelgan'),
        ('kelmagan', 'Kelmagan'),
        ('sababli', 'Sababli'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.full_name} - {self.status}"
