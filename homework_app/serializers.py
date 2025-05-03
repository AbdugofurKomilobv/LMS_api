from rest_framework import serializers
from homework_app.models import Homework,HomeworkAnswer
from lessons_app.models import Lesson
from courses_app.models import Group

class HomeworkCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S') 
    class Meta:
        model = Homework
        fields = ['id', 'lesson', 'group','title', 'description', 'deadline']

    def validate_lesson(self, value):
        request = self.context['request']
        teacher = getattr(request.user, 'teacher', None)

        if value.teacher != teacher:
            raise serializers.ValidationError("Siz bu darsga homework qo‘sha olmaysiz.")
        return value




class HomeworkAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAnswer
        fields = [
            'id',
            'homework',
            'student',
            'answer_text',
            'submitted_at',
            'grade',
            'is_graded'
        ]
        read_only_fields = ['id', 'submitted_at']

# HomeworkAnswerSerializer (Baholash uchun
class HomeworkTeacherAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkAnswer
        fields = ['id', 'homework', 'student', 'answer_text', 'submitted_at', 'grade', 'is_graded']

# ========================================

# Bu serializer homeworkning qisqacha ma'lumotlarini o'z ichiga oladi va o'quvchiga tegishli homeworklarni ko'rsatadi.
class StudentHomeworkListSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title')  # Dars nomi
    group_title = serializers.CharField(source='group.title')    # Guruh nomi
    deadline = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # Deadline

    class Meta:
        model = Homework
        fields = ['id', 'lesson_title', 'group_title', 'title', 'deadline']

# Bu serializer homeworkning batafsil ma'lumotlarini o'z ichiga oladi, ya'ni o'quvchi homework'ni batafsil ko'rish uchun ishlatiladi.
class StudentHomeworkDetailSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title')  # Dars nomi
    group_title = serializers.CharField(source='group.title')  # Guruh nomi
    description = serializers.CharField(allow_blank=True, required=False)  # Tavsif

    class Meta:
        model = Homework
        fields = ['id', 'lesson_title', 'group_title', 'title', 'description', 'deadline']



# Bu serializer o'quvchining homework'ga javobini ko'rsatadi va javob yuborish uchun ishlatiladi.
class StudentHomeworkAnswerSerializer(serializers.ModelSerializer):
    answer_text = serializers.CharField()  # Javob matni
    submitted_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # Yuborilgan vaqt

    class Meta:
        model = HomeworkAnswer
        fields = ['id', 'homework', 'student', 'answer_text', 'submitted_at']
