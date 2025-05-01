from django.db import models


from user_app.models import Teacher,Student
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
    teacher = models.ManyToManyField("user_app.Teacher",related_name='groups',blank=True)
    # students = models.ManyToManyField("user_app.Student", related_name="groups")
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True,blank=True)
    table = models.ForeignKey('Table',on_delete=models.SET_NULL,null=True,blank=True,related_name='groups')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

# ==================================================================
