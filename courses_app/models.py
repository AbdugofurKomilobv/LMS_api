from django.db import models


from user_app.models import Teacher
from common_app.models import BaseModel


# kurs model
class Course(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

# ============================================

# Jadval turi modeli
class TableType(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Table Type'
        verbose_name_plural = 'Table Types'

# ==================================================

# bu model jadval kursni boshlanish vaqti tugash vaqti qaysi xonada bolishi va jadval turi
class Table(BaseModel):
    start_time = models.CharField(max_length=50)
    finish_time = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    type =  models.ForeignKey(TableType,on_delete=models.CASCADE,related_name='tabels')

    def __str__(self):
        return f"{self.room} ({self.start_time} - {self.finish_time})"
    

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

# ======================================================================

# Group modeli - o'quvchilar yoki darslar guruhlarini ifodalaydi.
# Har bir guruhga nom, ustozlar, jadval, izox va faol/masligi bog'lanadi.
# Ustozlar ko'p bo'lishi mumkin (ManyToMany), jadval bitta (ForeignKey).

class Group(BaseModel):
    title = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Teacher,related_name='groups',null=True,blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    table = models.ForeignKey('Table',on_delete=models.SET_NULL,null=True,blank=True,related_name='groups')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

# ==================================================================
# O'quvchilarga uyga vazifa berish uchun mo'ljallangan model.
# Vazifa nomi, tavsifi, kurs, guruh va o'qituvchi bilan bog'lanadi.

class Homework(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    course = models.ForeignKey('courses_app.Course',on_delete=models.CASCADE,related_name='homeworks')
    group = models.ForeignKey('courses_app.Group',on_delete=models.CASCADE,related_name='homeworks')
    teacher = models.ForeignKey('user_app.Teacher',on_delete=models.CASCADE,related_name='homeworks')

    def __str__(self):
        return f"{self.title} - {self.group.title}"
    
    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

# ============================================================
# Talaba tomonidan topshirilgan uyga vazifa faylini va uning tekshirilganligini kuzatish uchun mo'ljallangan model

class HomeworkSubmission(BaseModel):
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE,related_name='submissions')
    student = models.ForeignKey('user_app.Student',on_delete=models.CASCADE, related_name='submissions')
    link = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.full_name} -- {self.homework.title}"
    class Meta:
        verbose_name = 'Homework Submission'
        verbose_name_plural = 'Homework Submissions'
# ===================================================================

# Bu model o'qituvchi tomonidan talabalar topshirgan uyga vazifalarini tekshirish va baholash uchun ishlatiladi.
# Baholashda sharh va baho saqlanadi.
class HomeworkReview(BaseModel):
    submission = models.OneToOneField(HomeworkSubmission,on_delete=models.CASCADE,related_name='review')
    teacher = models.ForeignKey('user_app.Teacher',on_delete=models.CASCADE,related_name='review')
    comment = models.TextField(null=True,blank=True)
    grade = models.PositiveIntegerField(null=True,blank=True)


    def __str__(self):
        return f"Tekshirish {self.submission.student.user.full_name} - {self.submission.homework.title}"




