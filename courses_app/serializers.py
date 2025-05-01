from rest_framework import serializers


from courses_app.models import Group, Course, Table, TableType
from user_app.models import Student


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title','teacher','active','table','course')

# Oddiy (non-model) serializer yaratilyapti, u bir nechta group idlarini olish uchun ishlatiladi.
class GetGroupByIdsSerializer(serializers.Serializer):
     # group_ids — bu ListField, ya'ni ro'yxat shaklidagi maydon.
    # Har bir element ro'yxatda albatta butun son (IntegerField) bo'lishi kerak.
    # Misol: {"group_ids": [1, 2, 3]}
    group_ids = serializers.ListField(child=serializers.IntegerField())






class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'



# Talabani guruhdan chiqarish uchun foydalaniladigan serializer
class RemoveStudentFromGroupSerializer(serializers.Serializer):
    # Foydalanuvchidan faqat bitta qiymat — student_id (talaba IDsi) olinadi
    student_id = serializers.IntegerField()  # Talabaning ID raqami, bu orqali qaysi talabani chiqarish kerakligi aniqlanadi


# O'qituvchini guruhdan chiqarish uchun ishlatiladigan serializer
class RemoveTeacherFromGroupSerializer(serializers.Serializer):
    # Foydalanuvchidan teacher_id (o'qituvchi IDsi) olinadi
    teacher_id = serializers.IntegerField()  # O'qituvchining ID raqami, shu orqali qaysi o'qituvchini chiqarish kerakligi aniqlanadi


# Guruhga student qo‘shish uchun serializer
class GroupAddStudent(serializers.Serializer):
    # Foydalanuvchidan student_id kutiladi
    student_id = serializers.IntegerField()  # Qo‘shiladigan studentning ID raqami

# Guruhga o'qituvchi (teacher) qo'shish uchun oddiy serializer
class GroupAddTeacher(serializers.Serializer):
    # Foydalanuvchidan o'qituvchining ID raqami olinadi
    teacher_id = serializers.IntegerField()  # Qo‘shiladigan teacher'ning ID raqami


# =====================================================


