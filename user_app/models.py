from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from django.db import models

from common_app.models import BaseModel


# ======================================================================================
# Foydalanuvchilarni yaratish va boshqarish uchun maxsus User manager klassi
class UserManager(BaseUserManager):


    # Oddiy foydalanuvchi yaratish uchun metod
    def create_user(self,phone,password=None,**extra_fields):
        if not phone:
            raise ValueError("Telefon raqami o'rnatilishi kerak")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
     # Superuser (admin) yaratish uchun metod
    def create_superuser(self,phone,password = None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_admin",True)
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser uchun (is_staff=True) bolishi kerak")
        if extra_fields.get("is_admin") is not True:
            raise ValueError('Superuser uchun (is_admin=True) bolishi kerak"')
        return self.create_user(phone,password,**extra_fields)
    




# =====================================================================================

# User model
class User(AbstractBaseUser,PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', 
                                 message="Telefon raqami quyidagi formatda kiritilishi kerak: '9989012345678'. 14 tagacha raqamga ruxsat beriladi.")
    phone = models.CharField(validators=[phone_regex],max_length=17,unique=True)
    full_name = models.CharField(max_length=60,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)    

    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    objects = UserManager()

    def __str__(self):
        return self.phone
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin
    
# ====================================================================================


# O'quvchilar modeli
class Student(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    group = models.ManyToManyField('courses_app.Group',related_name='group_student',blank=True)
    course = models.ManyToManyField('courses_app.Course',related_name='course_student',blank=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.user.phone
    

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
# =====================================================================


# Ustoz modeli 
class Teacher(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    course = models.ManyToManyField('courses_app.Course',related_name='c_teacher')


    def __str__(self):
        return self.user.phone
    
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

# ===========================================


# # Bu model o‘quvchilarning ota-onalarini uchun

class Parent(BaseModel):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    students = models.ManyToManyField('Student',related_name='parent')
    phone = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"



