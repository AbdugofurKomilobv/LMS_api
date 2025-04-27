from django.db import models

from common_app.models import BaseModel
from user_app.models import Student
from courses_app.models import Group


class Status(BaseModel):
    title = models.CharField(max_length=255)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Attendance(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='attendance')
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendance')
    status = models.ForeignKey('Status',on_delete=models.CASCADE,related_name='attendance')



    def __str__(self):
        return f"{self.student.user.phone} - {self.group.title}"

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"