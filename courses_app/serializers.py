from rest_framework import serializers


from courses_app.models import Group, Subject, Course, Table, TableType, Homework, HomeworkSubmission, HomeworkReview


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

# Oddiy (non-model) serializer yaratilyapti, u bir nechta group idlarini olish uchun ishlatiladi.
class GetGroupByIdSerializer(serializers.Serializer):
     # group_ids — bu ListField, ya'ni ro'yxat shaklidagi maydon.
    # Har bir element ro'yxatda albatta butun son (IntegerField) bo'lishi kerak.
    # Misol: {"group_ids": [1, 2, 3]}
    group_ids = serializers.ListField(child=serializers.IntegerField())



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


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

# Homework modeliga asoslangan serializer
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
             # teacher maydonini faqat o‘qish (read-only) uchun qiladi,
        # ya'ni foydalanuvchi API orqali bu maydonni o‘zgartira olmaydi,
        # lekin ma'lumotni ko‘rishi mumkin (masalan, GET so‘rovida)
        extra_kwargs = {'teacher':{'read_only':True}}


# HomeworkSubmission modeliga asoslangan serializer
class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission  # Modelga bog'lanmoqda

        # Barcha maydonlarni serializerda ko‘rsatadi
        fields = '__all__'

        # extra_kwargs yordamida ayrim maydonlarga maxsus cheklovlar qo‘yiladi:
        extra_kwargs = {
            'student': {'read_only': True},     # student maydoni faqat o‘qish uchun, foydalanuvchi API orqali bu maydonni o‘zgartira olmaydi
            'is_checked': {'read_only': True}   # is_checked ham read-only: odatda bu maydonni tekshiruvchi (teacher) o‘zgartiradi
        }


class HomeworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkReview
        fields = '__all__'
        extra_kwargs = {
            'teacher': {'read_only': True}
        }


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
